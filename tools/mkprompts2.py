import html, re
exec(open('mkprompts.py').read().split('def prompt')[0])  # loads BASE, G (old 30 prompts)
OLD_BASE, OLD = BASE, G
NEW_BASE=("Photorealistic, editorial cocktail photograph, landscape 3:2 (1536×1024), split into three equal vertical panels "
"separated by thin black gaps. Each panel is its OWN distinct photo shoot: its own backdrop, surface, color palette, "
"lighting and mood, exactly as described below. The three panels must not look alike. In every panel: one cocktail "
"standing centered, the entire glass visible from the top of the garnish down to the base; the glass fills about 70% "
"of the panel height and no more than half its width; leave clear, uncluttered backdrop above the garnish and keep "
"props low and to the sides so nothing touches the top edge. Rich, appetizing color, crisp focus on the glass, real "
"condensation, ice and liquid texture, the setting softly blurred behind. No text, labels, logos, branded bottles, "
"people or hands. Keep every surface natural and smooth: never cover the glass, liquid, ice or table in a uniform "
"pebbled, crackled or scaly texture.")
FIZZ_NOTE=(" Make the carbonation look real: thin, smooth, crystal-clear glass walls; fine, separate streams of tiny "
"bubbles rising through clear liquid, with clear liquid visible between them; a few small bubbles clinging to the ice and "
"the inside of the glass; a delicate fizz at the surface; only a light, natural mist of condensation on the outside, never a "
"heavy coat of droplets or dots covering the glass.")
ICE_NOTE=(" The ice must look real: crystal-clear, smooth-faced ice with soft rounded edges, like polished glass, with no cracks, "
"veins or crackle pattern inside it; the spirit around it is clear and glossy with no texture in the liquid; only a light, "
"fine mist of condensation on the outside, never a heavy coat of droplets covering the glass.")
import re as _re
ICY=_re.compile(r"ice cube|with ice|over ice|crushed ice", _re.I)
FIZZY=_re.compile(r"sparkling (?!sugar)|soda|fizz|bubbl|tonic|ginger beer|ginger ale|\bcola\b", _re.I)
# (name, drink description, scene)
REDO=[
 [("Daiquiri","chilled coupe of pale, cloudy lime-white with a thin lime wheel on the rim","a sun-drenched Havana café table of worn turquoise-painted wood against peeling pastel-yellow plaster, bright late-afternoon sun with crisp shadows, halved limes and a small bowl of raw sugar"),
  ("Tom Collins","tall Collins glass with ice, sparkling pale lemon-clear with bubbles, a lemon wheel and a red cherry","a white marble counter on a breezy summer porch, soft morning daylight, a blurred green garden behind, a pitcher and lemons"),
  ("Aviation","chilled coupe of pale sky-lavender, clear, with a dark brandied cherry at the bottom","a 1920s Art Deco bar of black lacquer and brass with a soft pale-blue glow behind like a dawn sky, a few violet flowers")],
 [("Sidecar","chilled coupe of glowing amber-gold with a fine sugar rim and a lemon twist","a Parisian zinc bar counter in warm golden lamplight, a blurred café mirror behind, lemons and a cut-crystal sugar bowl"),
  ("Kir Royale","champagne flute of sparkling deep ruby-pink wine with rising bubbles","a celebration table with a pale pink silk cloth, soft candlelight and sparkling gold bokeh behind, blackcurrants in a small silver dish"),
  ("Penicillin","rocks glass with one large clear ice cube in golden amber whisky, candied ginger on a cocktail pick","a weathered dark oak table by a misty Scottish window, moody side light, fresh ginger root, a lemon and a piece of honeycomb")],
 [("Last Word","chilled coupe of pale chartreuse-green, slightly cloudy","a speakeasy back room with a deep emerald-green velvet backdrop and a single warm spotlight, limes and a vintage brass jigger"),
  ("Americano","highball glass with ice, bright translucent red-orange with soda bubbles, an orange slice","a sunny Milanese café terrace, small white café table, bright midday sun, blurred terracotta buildings, orange halves and an espresso cup"),
  ("Black Russian","rocks glass over ice, nearly black coffee-brown, clear, no cream","a midnight-blue study with dark walnut and leather, low warm lamplight, roasted coffee beans scattered on the wood")],
 [("Jungle Bird","rocks glass over ice, deep ruby red-brown, a pineapple wedge and pineapple leaves","a rattan table under dappled sunlight through palm fronds, lush green jungle bokeh, a halved pineapple"),
  ("Singapore Sling","hurricane glass with ice, rosy pink-red with a light frothy top, a pineapple wedge and a red cherry","a colonial grand-hotel veranda with white wicker and slatted shade, hazy warm afternoon light, pineapple pieces and white orchids"),
  ("Shirley Temple","tall Collins glass with ice, bright pink-red sparkling soda, a lemon wheel and a red cherry with stem","a playful retro 1950s diner counter, candy-pink and white backdrop, bright cheerful light, a bowl of red cherries")],
 [("Arnold Palmer","tall Collins glass with ice, golden-amber half iced tea and half lemonade, a lemon wheel","a sunny country-club patio with a white table, bright soft sunlight, blurred green lawn, lemons and a glass pitcher of tea"),
  ("Vodka Tonic","highball glass with ice, crystal-clear sparkling tonic with bubbles, a lime wheel","a cool minimalist pale blue-gray stone surface and wall, crisp clean daylight, loose ice cubes and lime halves"),
  ("Gin Fizz","highball glass without ice, pale cloudy white with a tall fluffy white foam head","a vintage soda-fountain counter of white tile and chrome, bright airy daylight, lemons and a silver shaker")],
 [("Corpse Reviver No. 2","chilled coupe of pale cloudy lemon-yellow","a gothic setting of deep plum velvet and candlelight, an antique absinthe bottle with no label and lemons"),
  ("Vesper","chilled coupe of crystal-clear ice-cold liquid with a long lemon peel twist","a sleek casino bar, glossy black bar top, deep navy backdrop with soft gold bokeh, a few casino chips"),
  ("White Lady","chilled coupe of pale cloudy white with a thin silky foam layer","an elegant ivory satin setting with a string of pearls, soft diffused glowing light, lemons")],
 [("Rusty Nail","rocks glass with one large clear ice cube, deep honey-amber, a lemon peel","a hunting lodge of rough dark stone and red tartan wool, warm firelight glow, lemons"),
  ("Godfather","rocks glass with one large clear ice cube, warm amber-gold","a dim Italian supper club, deep red leather booth behind, warm amber light, almonds in a small dish"),
  ("Vieux Carré","rocks glass with one large clear ice cube, deep reddish mahogany-brown, a lemon peel","a New Orleans French Quarter balcony at dusk, wrought-iron railing and warm gaslight glow, lemons")],
 [("Amaretto Sour","rocks glass over ice, golden amber with a thick white foam top, a red cherry","a warm Italian kitchen of terracotta tiles and cream plaster, soft window light, almonds and lemons"),
  ("New York Sour","rocks glass over ice, golden whiskey sour with a distinct layer of red wine floating on top","a Manhattan rooftop ledge at night, blurred city lights behind, cool blue and warm gold tones, lemons"),
  ("Whiskey Smash","rocks glass with crushed ice, pale amber, a big fresh mint sprig","a weathered wooden farmhouse picnic table in bright summer sun, a basket of fresh mint and lemons")],
 [("Grasshopper","chilled coupe of creamy pale mint-green, smooth and opaque","a playful mid-century setting with a mint-green and white backdrop, soft bright light, fresh mint and chocolate squares"),
  ("Mudslide","rocks glass over ice, creamy coffee-brown, topped with chocolate shavings","a cozy ski chalet with a chunky knit blanket and pine wood, warm firelight, coffee beans and chocolate pieces"),
  ("Stinger","chilled coupe of clear golden-amber with a mint sprig","an old gentleman's club of oxblood leather and dark mahogany, low lamplight, fresh mint")],
 [("El Diablo","highball glass with ice, golden ginger beer with a deep purple-red layer sinking from the top, a lime wheel","a desert-sunset scene against a warm red-orange adobe wall, low golden sun, limes and dried red chilies"),
  ("Sea Breeze","highball glass with ice, bright pink-red, a lime wedge","a seaside deck of bleached driftwood, bright coastal light, blurred blue ocean behind, limes and a grapefruit"),
  ("Bay Breeze","highball glass with ice, coral pink, a lime wedge","a bamboo beach-bar counter at golden hour, warm sunset glow, pineapple pieces and limes")],
 [("Greyhound","highball glass with ice, pale pink-yellow grapefruit juice","a bright sunlit kitchen with a soft pastel-peach backdrop, fresh morning light, a halved grapefruit"),
  ("Salty Dog","highball glass with ice and a coarse salt rim, pale pink grapefruit juice","weathered blue-gray boat-deck boards with a coil of rope, crisp sea light, coarse sea salt and grapefruit"),
  ("Fuzzy Navel","highball glass with ice, bright opaque orange, an orange slice","a fun retro 1980s pastel peach-to-orange backdrop, bright cheerful light, oranges and a peach")],
 [("Sex on the Beach","highball glass with ice, orange at the top fading into deep red at the bottom, an orange slice","sand-colored surface with a glowing orange-pink sunset sky blurred behind, oranges and cranberries"),
  ("Hurricane","curvy hurricane glass with ice, vivid red-orange, an orange wheel and a red cherry","a Mardi Gras night, deep purple backdrop with gold and green bead bokeh, passion fruit and oranges"),
  ("Zombie","hurricane glass with crushed ice, deep amber-orange rum punch, a big mint sprig","a tiki bar of carved dark wood and warm torchlight glow, big tropical leaves, limes and pineapple")],
 [("Rum Punch","hurricane glass with ice, orange-amber with a red glow at the bottom, an orange wheel and a red cherry","a bright turquoise-painted Caribbean wooden table in vivid sunshine, red hibiscus flowers and oranges"),
  ("Blue Margarita","chilled coupe of vivid electric blue, a lime slice on the rim","a poolside at night, white tile edge with glowing aqua water-light rippling behind, limes"),
  ("Ranch Water","highball glass with ice, crystal-clear and very bubbly, a lime wedge","a weathered West Texas ranch fence rail in dusty golden-hour light, limes")],
 [("Hemingway Daiquiri","chilled coupe of pale blush-pink cloudy liquid, a lime wheel","a sun-bleached Key West fishing dock, bright tropical sun, limes and a grapefruit"),
  ("Kamikaze","chilled coupe of pale translucent lime-yellow, a lime wheel","a sleek black nightclub bar with electric green and blue neon glow behind, limes"),
  ("Lemon Drop Martini","chilled coupe of pale lemon-yellow with a sparkling sugar rim","a bright sunny-yellow backdrop and white marble counter, high-key cheerful light, lemons and sugar")],
 [("French Martini","chilled coupe of soft raspberry-pink with a fine velvety foam top","a chic Parisian boudoir with blush-pink velvet, soft glamorous light, raspberries and pineapple"),
  ("Blood and Sand","chilled coupe of rusty orange-red, an orange twist","a dramatic deep crimson backdrop with strong side light, blood oranges and dark cherries"),
  ("Martinez","chilled coupe of deep reddish amber, a lemon twist","a Victorian bar of dark green tile and polished brass, warm gaslight, lemons")],
 [("Paper Plane","chilled coupe of bright orange-amber, clear and glowing","a vintage map and kraft paper surface in warm afternoon light, a folded paper airplane and lemons"),
  ("Champagne Cocktail","champagne flute of golden sparkling wine with a sugar cube fizzing at the bottom and a lemon twist","a New Year's celebration, black backdrop with gold confetti and sparkle bokeh, sugar cubes and lemons"),
  ("Gibson","chilled coupe of crystal-clear ice-cold liquid with two pearl onions on a pick","a classic steakhouse bar of dark walnut in cool silver light, small pearl onions in a dish")],
]
B3=[
 [("Bee's Knees","chilled coupe of cloudy pale honey-yellow, a lemon twist","a sunny garden table with a honeycomb on a wooden board, warm golden light, blurred wildflowers, a honey dipper and lemons"),
  ("Tommy's Margarita","rocks glass with ice, pale cloudy lime-green, no salt, a lime wheel","a Mexican cantina with hand-painted blue-and-white Talavera tiles, bright warm light, limes and a small agave plant"),
  ("Pimm's Cup","highball glass with ice, amber-brown and sparkling, packed with cucumber, orange and strawberry slices and a mint sprig","an English summer garden party, white picnic cloth on a green lawn, soft sunlight, strawberries")],
 [("Planter's Punch","hurricane glass with ice, orange at the top deepening to red at the bottom, an orange wheel and a red cherry","a Jamaican plantation veranda with bright green wooden shutters, strong tropical sun, oranges"),
  ("Queen's Park Swizzle","highball glass packed with crushed ice in three layers: bright green mint at the bottom, golden rum in the middle, red-brown bitters on top, a mint sprig","lush tropical leaves in dappled sun, a wooden swizzle stick"),
  ("John Collins","tall Collins glass with ice, pale golden and fizzy, a lemon wheel and a red cherry","a white-painted Kentucky porch railing at golden hour, lemons")],
 [("French 77","champagne flute of pale gold sparkling wine with a lemon twist","a Paris spring scene, pale cream backdrop with sprays of white elderflower, soft daylight"),
  ("St-Germain Cocktail","tall Collins glass with ice, pale straw-gold sparkling wine and soda, a long lemon twist","an Alpine meadow picnic on white linen, airy bright light, elderflower sprigs"),
  ("French Gimlet","chilled coupe of pale cloudy green-white, a lime wheel","a French bistro marble table in soft morning light, limes and elderflower blossoms")],
 [("Scarlett O'Hara","chilled coupe of bright cranberry red, a lime wheel","a Southern parlor with white magnolia blossoms, warm afternoon light, fresh cranberries"),
  ("Disaronno Sour","rocks glass over ice, golden amber with a thick white foam top","an Italian lakeside terrace in warm sunset light, almonds and lemons"),
  ("Kentucky Sunrise","highball glass with ice, orange fading to deep red at the bottom, an orange wheel and a red cherry","weathered red barn wood in soft sunrise light, oranges")],
 [("Honey Deuce","highball glass with ice, pale pink lemonade, a skewer of honeydew melon balls","tennis whites and green, a blurred grass court in bright summer sun, a tennis ball and honeydew melon"),
  ("Hennessy Mule","rocks glass with ice, amber and fizzy, a lime wheel and a slice of ginger","an urban loft with exposed brick, moody warm light, fresh ginger root"),
  ("Maker's & Ginger","rocks glass with ice, golden amber and sparkling, a lime wedge","a deep red backdrop with warm glowing light and a dark wood bar, limes")],
 [("Irish Whiskey Sour","rocks glass over ice, golden with a white foam top, a lemon twist and a red cherry","a cozy Irish pub with a dark green wall and warm brass light, lemons"),
  ("Irish Old Fashioned","rocks glass with one large clear ice cube, deep amber, an orange twist","a stone cottage windowsill with misty green hills softly blurred outside, soft daylight, oranges"),
  ("Irish Boulevardier","rocks glass with one large clear ice cube, deep red-amber, an orange twist","a dark wood bar with a warm stained-glass glow behind, oranges")],
 [("Baileys S'mores Martini","chilled coupe of creamy beige with a chocolate drizzle and a graham-cracker crumb rim, toasted marshmallows on a pick","a campfire at night, glowing ember light, marshmallows on sticks"),
  ("Baileys Mudslide","chilled coupe of creamy coffee color with chocolate syrup swirled inside the glass","a chocolate shop with a rich brown backdrop and warm light, chocolate bars and cocoa"),
  ("Baileys Flat White Martini","chilled coupe of creamy coffee with a smooth pale foam top and three coffee beans","a coffee house with a blurred espresso machine and morning light, coffee beans")],
 [("Chambord Royale","chilled coupe of sparkling raspberry-pink wine, a raspberry","a romantic deep raspberry velvet backdrop with candlelight, fresh raspberries"),
  ("Chambord Margarita","rocks glass with ice, deep berry red-purple, a lime slice","a festive scene with colorful blurred paper-banner bokeh, warm light, a halved pomegranate"),
  ("Cointreau Royale","champagne flute of pale gold sparkling wine with an orange twist","a sunny Mediterranean balcony with a blue sea blurred behind, oranges")],
 [("Cointreau Fizz","highball glass with ice, clear pale sparkling, a lime wheel and an orange twist","a crisp, modern bright orange backdrop with clean light, limes and oranges"),
  ("Bermuda Rum Swizzle","highball glass with crushed ice, tropical orange-red, a mint sprig","a pink-sand beach with pastel cottages blurred behind, bright sun"),
  ("Doctor Funk","highball glass with ice, rosy pink and fizzy, a mint sprig","a Polynesian bar of bamboo and tapa cloth in warm torchlight")],
 [("Sherry Cobbler","goblet heaped with crushed ice, pale amber, piled with berries, orange slices and mint, a straw","a Victorian summer table with a white lace cloth in bright sunshine"),
  ("Suffering Bastard","highball glass with ice, amber ginger fizz, mint and a cucumber slice","a 1940s grand hotel bar of brass and palm fronds in hazy warm light"),
  ("Trinidad Sour","chilled coupe of deep, opaque reddish-brown with a thin foam, a lemon twist","a Caribbean spice market with burlap and warm light, cinnamon sticks and whole nutmeg")],
 [("Tipperary","chilled coupe of deep amber-red with a faint green glint","an Irish manor library of green leather and old books in lamplight"),
  ("Corn 'n' Oil","rocks glass with crushed ice, nearly black rum with a dark glossy sheen, a lime wedge","an old sugar mill of rough stone in strong sunlight, stalks of sugar cane"),
  ("Almond Piña Colada","hurricane glass of creamy pale yellow-white, a pineapple wedge","a beach cabana on white sand, bright turquoise sea blurred behind")],
 [("Hendrick's Cucumber Lemonade","highball glass with ice, cloudy pale lemon, cucumber rounds and a lemon wheel","an English rose garden in bright soft light, roses and cucumbers"),
  ("Hendrick's Gin Mule","highball glass with ice, pale gold fizz, cucumber rounds and a mint sprig","a Victorian glass greenhouse with lush ferns in dappled light"),
  ("Vodka Basil Smash","rocks glass with ice, vivid bright green, a basil sprig","an Italian herb garden with terracotta pots of basil in sunlight")],
 [("Lemon Meringue Pie'tini","chilled coupe of creamy pale lemon-yellow with a sugar rim","a pastel-yellow bakery counter in soft light, a slice of lemon meringue pie beside"),
  ("Patrón & Grapefruit","highball glass with ice, pale pink grapefruit, a grapefruit wedge","a rooftop with a pink-washed wall in golden evening light, grapefruit halves"),
  ("Piscola","tall Collins glass with ice, dark cola-brown and fizzy, a lime wedge","a rustic wooden table with Andes mountains blurred behind at dusk")],
 [("Grand Frozen Margarita","chilled coupe of frosty, slushy pale orange-yellow","a sunny poolside with bright blue water behind, limes"),
  ("St-Germain Royale","champagne flute of pale gold sparkling wine with a blackberry","an elegant garden wedding with white flowers blurred behind in soft light"),
  ("Gin Berry Spritz","stemmed wine glass with ice, sparkling raspberry-pink, a raspberry and a lemon wedge","a summer picnic on red gingham in sunlight, fresh berries")],
 [("Tanqueray Gin Spritz","stemmed wine glass with ice, pale sparkling liquid with cucumber slices, basil and mint","a Mediterranean terrace with a white wall and blue shutters in bright sun"),
  ("Baltimore Eggnog","rocks glass of creamy ivory with grated nutmeg on top","a Christmas scene with twinkling lights blurred behind, red and green, warm fireplace glow"),
  ("Amaretto Fizz","champagne flute of sparkling golden orange","an Italian brunch table with pastel linens in morning sun, oranges and almonds")],
]
FIX=[[REDO[0][1],REDO[2][1],REDO[3][2]]]
assert len(REDO)==16 and sum(len(g) for g in REDO)==48
assert len(B3)==15 and len({d[0] for g in B3 for d in g})==45
POS=["LEFT","MIDDLE","RIGHT"]
def new_prompt(g):
    return "\n".join([NEW_BASE,""]+[f"{p} panel: {n}, a {d}. Scene: {sc}."+(FIZZ_NOTE if FIZZY.search(d) else "")+(ICE_NOTE if ICY.search(d) and not FIZZY.search(d) else "") for p,(n,d,sc) in zip(POS,g)])
def old_prompt(g):
    return "\n".join([OLD_BASE,""]+[f"{p} panel: {n}, a {d}; beside it, {pr}." for p,(n,d,pr) in zip(POS,g)])
def card(pid,label,g,text,check=True):
    names=" · ".join(d[0] for d in g)
    cb=(f'<label class="done"><input type="checkbox" id="done{pid}" aria-label="Mark prompt {label} done"><span class="num">Prompt {label}</span></label>' if check
        else f'<span class="num">Prompt {label}</span>')
    return f'''
  <article class="prompt" id="p{pid}" data-id="{pid}">
    <header>
      {cb}
      <h2>{html.escape(names)}</h2>
      <button class="copy" type="button" data-target="t{pid}">Copy</button>
    </header>
    <pre id="t{pid}">{html.escape(text)}</pre>
  </article>'''
exec(open('b4data.py').read())
REDO2=[[(n,d,SC2[n]) for (n,d,_p) in OLD[i]] for i in range(15,30)]
H=lambda t: f'\n  <h2 class="batch">{t}</h2>'
RT=lambda g: new_prompt(g).replace(NEW_BASE, (NEW_BASE+STRICT).replace('real condensation, ice and liquid texture','clear ice and glossy liquid')).replace('only a light, natural mist of condensation on the outside, never a heavy coat of droplets or dots covering the glass','a dry, smooth outside of the glass').replace('only a light, fine mist of condensation on the outside, never a heavy coat of droplets covering the glass','a dry, smooth outside of the glass')
cards=H('Re-takes · F3–F5 · the 7 drinks held back in Batch 4 (F5 is a spare second try for three of them)')
for i,g in enumerate(RETAKE3,3): cards+=card(f'F{i}',f'F{i}',g,RT(g))
cards+=H('Fix · prompt F2 · re-take El Diablo, St-Germain Cocktail and Bermuda Rum Swizzle')+card('F2','F2',RETAKE,new_prompt(RETAKE))
cards+=H('Done · Batch 4 · prompts 46–72')
for i,g in enumerate(B4G,46): cards+=card(str(i),str(i),g,new_prompt(g))
cards+=H('Redo · prompts R17–R31 · Batch 2 drinks in their own scenes')
for i,g in enumerate(REDO2,17): cards+=card(f'R{i}',f'R{i}',g,new_prompt(g))
cards+=H('Done · F1 · re-take of the three sparkling drinks')+card('F1','F1',FIX[0],new_prompt(FIX[0]))
cards+=H('Done · R1–R16 · the 48 classics in their own scenes')
for i,g in enumerate(REDO,1): cards+=card(f'R{i}',f'R{i}',g,new_prompt(g))
cards+=H('Done · Batch 3 · prompts 31–45')
for i,g in enumerate(B3,31): cards+=card(str(i),str(i),g,new_prompt(g))
TOTAL=cards.count('type="checkbox"')
old=''
for i,g in enumerate(OLD,1): old+=card(f'old{i}',str(i),g,old_prompt(g),check=False)
t=open('prompts_tpl.html').read()
t=t.replace('<p class="lede">Thirty ChatGPT image prompts covering 90 drinks, in two batches of 45. Each one makes a three-panel image in the same dark-slate style as your Daiquiri, Tom Collins and Aviation set.</p>',
 f'<p class="lede">{TOTAL} ChatGPT image prompts, one image each with three drinks, every drink in its own scene. New at the top: F3–F5 re-take the drinks held back in Batch 4, then R17–R31 redo Batch 2 in the new style. Finished prompts are further down.</p>')
t=t.replace("0 of 30 done",f"0 of {TOTAL} done").replace("n+' of 30 done'",f"n+' of {TOTAL} done'").replace("(n/30*100)",f"(n/{TOTAL}*100)")
t=t.replace("document.querySelectorAll('.prompt').forEach","document.querySelectorAll('.wrap > .list > .prompt').forEach")
t=t.replace("el.querySelector('input').checked=on;","var inp=el.querySelector('input'); if(inp) inp.checked=on;")
t=t.replace('{{CARDS}}\n  </div>','{{CARDS}}\n  </div>\n  <details class="earlier"><summary>Earlier prompts 1–30 (old dark-slate style, already done)</summary><div class="list old">{{OLD}}\n  </div></details>')
t=t.replace('</style>','  .earlier{ margin-top:2.5rem; } .earlier summary{ cursor:pointer; color:var(--soft); font-size:.95rem; padding:.5rem 0; }\n  .list.old .prompt{ opacity:.75; }\n</style>')
assert '{{OLD}}' in t
page=t.replace('{{CARDS}}',cards).replace('{{OLD}}',old)
open('drink-prompts.html','w').write(page); print('ok',len(page)//1024,'KB')
