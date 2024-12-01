from flask import Flask, render_template, request, redirect, url_for, session
import openai
import requests
import os
import json
from typing import List, Dict, Optional, Tuple

app = Flask(__name__)
app.secret_key = os.urandom(24)

# OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def analyze_cocktail_query(query: str) -> Tuple[List[str], List[str]]:
    system_prompt = """
    You are a professional bartender and cocktail expert. Analyze the cocktail request and return:
    1. "search_terms": Specific ingredients or cocktail names to search for.
    2. "characteristics": Descriptive terms about the desired drink.

    If the request is vague or descriptive (e.g., "Summer Vibes"), identify key descriptive terms like "refreshing," "tropical," or "fruity" and include relevant ingredients or cocktail names (e.g., "rum," "gin," "Pina Colada").
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this cocktail request: {query}"}
            ],
            temperature=0.7,
            max_tokens=150
        )
        content = response.choices[0].message.content
        print(f"OpenAI Response: {content}")  # Debugging Step
        result = json.loads(content)
        return result.get('search_terms', []), result.get('characteristics', [])
    except Exception as e:
        print(f"Error in query analysis: {e}")
        # Provide fallback for vague or descriptive terms
        if "summer" in query.lower() or "vibe" in query.lower():
            return ["rum", "gin", "tropical", "Pina Colada", "Margarita"], ["summer", "refreshing"]
        return ["cocktail"], []

def preprocess_query(query: str) -> List[str]:
    """Extract keywords from descriptive queries."""
    keywords = {
        "summer": ["refreshing", "tropical", "rum", "Margarita", "Pina Colada"],
        "vibe": ["tropical", "fun", "beach", "rum"],
        "winter": ["warm", "cozy", "whiskey", "Hot Toddy", "Irish Coffee"],
    }
    extracted_terms = []
    for word, terms in keywords.items():
        if word in query.lower():
            extracted_terms.extend(terms)
    return list(set(extracted_terms))

def get_cocktail_suggestions(characteristics: List[str]) -> List[str]:
    """Get additional cocktail suggestions based on characteristics."""
    suggestion_prompt = f"""
    For these characteristics: {', '.join(characteristics)}
    
    If they include 'warm', 'winter', or 'hot', be sure to suggest specific warm cocktails like:
    - Hot Toddy
    - Mulled Wine
    - Irish Coffee
    - Hot Buttered Rum
    - Hot Spiced Wine
    - Warm Cider
    
    Return only the cocktail names as a JSON array.
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a cocktail expert. Suggest cocktails based on given characteristics."},
                {"role": "user", "content": suggestion_prompt}
            ],
            temperature=0.8,
            max_tokens=100
        )
        
        suggestions = json.loads(response.choices[0].message.content)
        return suggestions if isinstance(suggestions, list) else []
    except Exception as e:
        print(f"Error getting suggestions: {e}")
        return []

def search_cocktails(terms: List[str]) -> List[Dict]:
    all_cocktails = []
    seen_ids = set()
    default_terms = ["rum", "gin", "Pina Colada", "Margarita", "tropical"]

    if not terms:
        terms = default_terms  # Use default fallback terms for broad queries

    for term in terms:
        if not term:
            continue

        try:
            # Search by name
            response = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={term}")
            response.raise_for_status()
            data = response.json()
            print(f"Search by name response for '{term}': {data}")  # Debugging Step
            
            drinks = data.get('drinks', [])
            if drinks is None or not isinstance(drinks, list):
                continue
            for drink in drinks:
                if drink['idDrink'] not in seen_ids:
                    all_cocktails.append(drink)
                    seen_ids.add(drink['idDrink'])
        except Exception as e:
            print(f"Error searching by name for '{term}': {e}")

        try:
            # Search by ingredient
            response = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={term}")
            response.raise_for_status()
            data = response.json()
            print(f"Search by ingredient response for '{term}': {data}")  # Debugging Step

            drinks = data.get('drinks', [])
            if drinks is None or not isinstance(drinks, list):
                continue
            for drink in drinks:
                if drink['idDrink'] not in seen_ids:
                    all_cocktails.append(drink)
                    seen_ids.add(drink['idDrink'])
        except Exception as e:
            print(f"Error searching by ingredient for '{term}': {e}")
    
    return all_cocktails

def get_cocktail_details(cocktail_id: str) -> Optional[Dict]:
    """Fetch and format detailed cocktail information."""
    try:
        response = requests.get(
            f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cocktail_id}"
        )
        if response.ok and isinstance(response.json(), dict):
            drinks = response.json().get('drinks', [])
            if drinks and isinstance(drinks, list):
                drink = drinks[0]
                
                # Format ingredients and measurements
                ingredients = []
                for i in range(1, 16):
                    ingredient = drink.get(f'strIngredient{i}')
                    measure = drink.get(f'strMeasure{i}')
                    if ingredient:
                        ingredients.append(
                            f"{measure.strip() if measure else ''} {ingredient}".strip()
                        )
                
                # Add formatted data
                drink['formatted_ingredients'] = ingredients
                return drink
                
    except Exception as e:
        print(f"Error fetching cocktail details: {e}")
    return None

@app.route('/')
def index():
    """Home page with search form."""
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handle both search form submission and results display."""
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if not query:
            return render_template('index.html', error="Please describe your desired drink.")
        
        try:
            # Process search
            print(f"User Query: {query}")  # Debugging Step
            search_terms, characteristics = analyze_cocktail_query(query)
            print(f"Search Terms: {search_terms}, Characteristics: {characteristics}")  # Debugging Step
            
            suggested_cocktails = get_cocktail_suggestions(characteristics)
            print(f"Suggested Cocktails: {suggested_cocktails}")  # Debugging Step
            
            all_search_terms = list(set(search_terms + suggested_cocktails))
            cocktails = search_cocktails(all_search_terms)
            print(f"Final Cocktails: {cocktails}")  # Debugging Step
            
            # Store in session
            session['cocktails'] = cocktails
            session['query'] = query
            session['characteristics'] = characteristics
            
            return render_template('results.html',
                                   cocktails=cocktails,
                                   query=query,
                                   characteristics=characteristics)
        except Exception as e:
            print(f"Search error: {e}")
            return render_template('results.html',
                                   error="An error occurred during search. Please try again.",
                                   cocktails=[],
                                   query=query)
    
    # Handle GET request
    return render_template('results.html',
                           cocktails=session.get('cocktails', []),
                           query=session.get('query', ''),
                           characteristics=session.get('characteristics', []))

@app.route('/cocktail/<string:cocktail_id>')
def cocktail_details(cocktail_id):
    """Display cocktail details."""
    try:
        cocktail = get_cocktail_details(cocktail_id)
        if not cocktail:
            return redirect(url_for('index'))
        
        return render_template('results.html',
                             cocktails=session.get('cocktails', []),
                             selected_cocktail=cocktail,
                             query=session.get('query', ''),
                             characteristics=session.get('characteristics', []))
    except Exception as e:
        print(f"Error displaying cocktail details: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)