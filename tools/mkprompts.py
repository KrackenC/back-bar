import html, json
BASE=("Photorealistic cocktail photograph, landscape 3:2 (1536×1024), split into three equal vertical panels "
"separated by thin dark gaps, like a triptych. In each panel, one cocktail stands centered with the entire glass "
"visible from the top of the garnish down to the base, leaving a little space above and below. Same setting in all "
"three: dark slate bar top, near-black background, moody low-key studio lighting with soft highlights on the glass, "
"crisp focus, and a few loose ingredients softly out of focus beside the glass. No text, labels, logos, people or hands.")
G=[
 [("Sidecar","chilled coupe of glowing amber-gold liquid with a fine sugar rim and a lemon twist","lemons"),
  ("Kir Royale","champagne flute of sparkling deep ruby-pink wine with rising bubbles, no garnish","blackcurrants"),
  ("Penicillin","rocks glass with one large clear ice cube in golden amber whisky, a piece of candied ginger on a cocktail pick","fresh ginger root and a lemon")],
 [("Last Word","chilled coupe of pale chartreuse-green, slightly cloudy, no garnish","limes"),
  ("Americano","highball glass with ice, bright translucent red-orange with soda bubbles, an orange slice","oranges"),
  ("Black Russian","rocks glass over ice, nearly black coffee-brown and clear (no cream), no garnish","coffee beans")],
 [("Jungle Bird","rocks glass over ice, deep ruby red-brown, garnished with a pineapple wedge and pineapple leaves","a pineapple"),
  ("Singapore Sling","hurricane glass with ice, rosy pink-red with a light frothy top, a pineapple wedge and a red cherry","pineapple pieces"),
  ("Shirley Temple","tall Collins glass with ice, bright pink-red sparkling ginger ale, a lemon wheel and a red maraschino cherry with stem","lemons")],
 [("Arnold Palmer","tall Collins glass with ice, golden-amber half iced tea, half lemonade, a lemon wheel","lemons"),
  ("Vodka Tonic","highball glass with ice, crystal-clear sparkling tonic with bubbles, a lime wheel","limes"),
  ("Gin Fizz","highball glass without ice, pale cloudy white with a fine frothy white head, no garnish","lemons")],
 [("Corpse Reviver No. 2","chilled coupe of pale cloudy lemon-yellow, no garnish","lemons and a small bottle of absinthe"),
  ("Vesper","chilled coupe of crystal-clear, ice-cold liquid with a long lemon peel twist","lemons"),
  ("White Lady","chilled coupe of pale cloudy white with a thin silky foam layer, no garnish","lemons")],
 [("Rusty Nail","rocks glass with one large clear ice cube, deep honey-amber, a lemon peel","lemons"),
  ("Godfather","rocks glass with one large clear ice cube, warm amber-gold, no garnish","almonds"),
  ("Vieux Carré","rocks glass with one large clear ice cube, deep reddish mahogany-brown, a lemon peel","lemons")],
 [("Amaretto Sour","rocks glass over ice, golden amber with a thick white egg-white foam top, a red cherry","lemons and almonds"),
  ("New York Sour","rocks glass over ice, golden whiskey sour with a distinct layer of red wine floating on top","lemons"),
  ("Whiskey Smash","rocks glass with crushed ice, pale amber, a big fresh mint sprig","fresh mint and lemons")],
 [("Grasshopper","chilled coupe of creamy pale mint-green, smooth and opaque, no garnish","fresh mint leaves"),
  ("Mudslide","rocks glass over ice, creamy coffee-brown, topped with chocolate shavings","coffee beans and chocolate pieces"),
  ("Stinger","chilled coupe of clear golden-amber brandy with a mint sprig","fresh mint")],
 [("El Diablo","highball glass with ice, golden ginger beer with a deep purple-red blackcurrant layer sinking from the top, a lime wheel","limes"),
  ("Sea Breeze","highball glass with ice, bright pink-red cranberry and grapefruit, a lime wedge","limes and a grapefruit"),
  ("Bay Breeze","highball glass with ice, coral pink cranberry and pineapple, a lime wedge","limes and pineapple pieces")],
 [("Greyhound","highball glass with ice, pale pink-yellow grapefruit juice, no garnish","a halved grapefruit"),
  ("Salty Dog","highball glass with ice and a coarse salt rim, pale pink grapefruit juice","a halved grapefruit"),
  ("Fuzzy Navel","highball glass with ice, bright opaque orange, an orange slice","oranges and a peach")],
 [("Sex on the Beach","highball glass with ice, orange at the top fading into deep red at the bottom, an orange slice","oranges and cranberries"),
  ("Hurricane","curvy hurricane glass with ice, vivid red-orange, an orange wheel and a red cherry","passion fruit and oranges"),
  ("Zombie","hurricane glass with crushed ice, deep amber-orange rum punch, a big mint sprig","limes and pineapple pieces")],
 [("Rum Punch","hurricane glass with ice, orange-amber with a red grenadine glow at the bottom, an orange wheel and a red cherry","oranges"),
  ("Blue Margarita","chilled coupe of vivid electric blue, a lime slice on the rim","limes"),
  ("Ranch Water","highball glass with ice, crystal-clear and very bubbly, a lime wedge","limes")],
 [("Hemingway Daiquiri","chilled coupe of pale blush-pink cloudy liquid, a lime wheel","limes and a grapefruit"),
  ("Kamikaze","chilled coupe of pale translucent lime-yellow, a lime wheel","limes"),
  ("Lemon Drop Martini","chilled coupe of pale lemon-yellow with a sparkling sugar rim","lemons")],
 [("French Martini","chilled coupe of soft raspberry-pink with a fine velvety foam top, no garnish","raspberries and pineapple pieces"),
  ("Blood and Sand","chilled coupe of rusty orange-red, an orange twist","oranges and dark cherries"),
  ("Martinez","chilled coupe of deep reddish amber, a lemon twist","lemons")],
 [("Paper Plane","chilled coupe of bright orange-amber, clear and glowing, no garnish","lemons"),
  ("Champagne Cocktail","champagne flute of golden sparkling wine with a sugar cube fizzing at the bottom and a lemon twist","sugar cubes and lemons"),
  ("Gibson","chilled coupe of crystal-clear, ice-cold liquid with two pickled cocktail onions on a pick","small pearl onions")],
]
G2=[
 [("Southside","chilled coupe of pale, slightly cloudy lime-green with a fresh mint leaf floating on top","fresh mint and limes"),
  ("Alexander","chilled coupe of smooth, creamy pale tan with a dusting of freshly grated nutmeg","a whole nutmeg and a small grater"),
  ("Between the Sheets","chilled coupe of clear pale golden-amber with a lemon twist","lemons")],
 [("Brandy Crusta","small coupe of clear amber brandy with a sparkling sugar rim and a long lemon peel curled inside the rim","lemons"),
  ("Casino","chilled coupe of pale, almost clear straw-yellow with a red cherry resting at the bottom","lemons and cherries"),
  ("Hanky Panky","chilled coupe of deep reddish-brown, clear and glossy, with an orange peel","oranges")],
 [("Mary Pickford","chilled coupe of rosy pink, cloudy pineapple with a light froth, a red cherry","pineapple pieces"),
  ("Monkey Gland","chilled coupe of cloudy orange-pink, no garnish","oranges"),
  ("Remember the Maine","chilled coupe of deep ruby amber, clear and glossy, with a dark cherry","dark cherries")],
 [("Tuxedo","chilled coupe of crystal-clear, pale liquid with a lemon twist and a red cherry","lemons"),
  ("El Presidente","chilled coupe of clear amber-orange with a rosy tint and an orange peel","oranges"),
  ("Naked and Famous","chilled coupe of glowing pale orange, clear, no garnish","limes")],
 [("Brown Derby","chilled coupe of golden amber, slightly cloudy, with a grapefruit twist","a halved grapefruit and a honey dipper"),
  ("Pineapple Martini","chilled coupe of pale golden-yellow, cloudy with a light foam, a lime wheel","pineapple pieces and limes"),
  ("Cable Car","chilled coupe with a cinnamon-sugar rim, foamy amber-orange, an orange twist","oranges and cinnamon sticks")],
 [("Old Cuban","chilled coupe of pale golden, gently sparkling liquid with a mint leaf","fresh mint and limes"),
  ("Ward Eight","chilled coupe of rosy orange-red, slightly cloudy, with a red cherry","lemons and oranges"),
  ("Death in the Afternoon","champagne flute of cloudy, pale milky-green sparkling wine with rising bubbles, no garnish","a small bottle of absinthe")],
 [("Airmail","champagne flute of pale gold sparkling wine with fine bubbles, no garnish","lemons and a honey dipper"),
  ("Seelbach","champagne flute of sparkling rose-copper wine with a long orange twist","oranges"),
  ("Russian Spring Punch","highball glass with ice, sparkling deep berry-red, topped with fresh raspberries and blackberries","fresh berries")],
 [("Garibaldi","rocks glass with ice, fluffy, opaque orange-red, an orange wheel","oranges"),
  ("Godmother","rocks glass with one large clear ice cube, pale golden amber, no garnish","almonds"),
  ("French Connection","rocks glass with one large clear ice cube, deep amber cognac, no garnish","almonds")],
 [("Oaxaca Old Fashioned","rocks glass with one large clear ice cube, deep amber, an orange peel","oranges"),
  ("Ti Punch","small rocks glass without ice, pale clear straw-yellow, a coin of lime peel","limes and sugar cane"),
  ("Gold Rush","rocks glass with one large clear ice cube, cloudy golden-honey, a lemon wedge","lemons and a honey dipper")],
 [("Kingston Negroni","rocks glass with one large clear ice cube, deep ruby red-brown, an orange wheel","oranges"),
  ("White Negroni","rocks glass with one large clear ice cube, pale clear golden-yellow, a grapefruit twist","a halved grapefruit"),
  ("Blood Orange Margarita","rocks glass with ice and a salt rim, deep ruby-orange, a blood orange slice","halved blood oranges")],
 [("Milk Punch","rocks glass with ice, creamy off-white, a dusting of grated nutmeg","a whole nutmeg"),
  ("Mock Margarita","rocks glass with ice and a salt rim, pale cloudy lime-yellow, a lime wheel","limes"),
  ("Irish Mule","rocks glass with ice, pale golden fizzy ginger beer, a mint sprig and a lime wedge","limes and fresh ginger")],
 [("Kentucky Mule","highball glass with ice, golden-amber fizzing ginger beer, a lime wheel and a mint sprig","limes and fresh mint"),
  ("Jamaican Mule","highball glass with ice, deeper amber-brown fizzing ginger beer, a lime wedge","limes and fresh ginger"),
  ("Bourbon Highball","highball glass with ice, pale amber and sparkling, a lemon wedge","lemons")],
 [("Gin Rickey","highball glass with ice, crystal-clear and sparkling, a lime wedge","limes"),
  ("Gin Gin Mule","highball glass with ice, pale cloudy gold with mint leaves inside, a big mint sprig","fresh mint and fresh ginger"),
  ("Alabama Slammer","highball glass with ice, bright red-orange, no garnish","oranges")],
 [("Pisco Punch","tall Collins glass with ice, pale golden-yellow, cloudy and fizzy, no garnish","pineapple pieces and lemons"),
  ("Chilcano de Pisco","tall Collins glass with ice, pale golden fizzy ginger ale, a lime wedge","limes"),
  ("Ginger No-jito","tall Collins glass with ice, pale gold fizz with muddled mint leaves inside, mint sprigs","fresh mint and limes")],
 [("Cinderella","tall Collins glass with ice, sunset orange with soda bubbles, a lemon wheel","oranges and pineapple pieces"),
  ("Rosé Spritzer","stemmed wine glass of pale salmon-pink sparkling wine with ice, no garnish","strawberries"),
  ("Bushwacker","hurricane glass of thick, frozen, creamy mocha-brown, a dusting of grated nutmeg","coconut halves and chocolate")],
]
G=G+G2
assert sum(len(g) for g in G)==90 and len({d[0] for g in G for d in g})==90
def prompt(g):
    pos=["LEFT","MIDDLE","RIGHT"]
    lines=[BASE,""]+[f"{p} panel: {n}, a {desc}; beside it, {props}." for p,(n,desc,props) in zip(pos,g)]
    return "\n".join(lines)
cards=""
for i,g in enumerate(G,1):
    if i in (1,16): cards+=f'\n  <h2 class="batch">Batch {1 if i==1 else 2} · prompts {i}–{i+14}</h2>'
    names=" · ".join(d[0] for d in g)
    p=html.escape(prompt(g))
    cards+=f'''
  <article class="prompt" id="p{i}" data-id="{i}">
    <header>
      <label class="done"><input type="checkbox" id="done{i}" aria-label="Mark prompt {i} done"><span class="num">Prompt {i}</span></label>
      <h2>{html.escape(names)}</h2>
      <button class="copy" type="button" data-target="t{i}">Copy</button>
    </header>
    <pre id="t{i}">{p}</pre>
  </article>'''
page=open('prompts_tpl.html').read().replace('{{CARDS}}',cards)
open('drink-prompts.html','w').write(page); print('ok', len(page)//1024,'KB')
