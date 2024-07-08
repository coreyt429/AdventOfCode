import sys
import networkx as nx
import matplotlib.pyplot as plt

def parse_input(lines):
    print(f' lines:\n {lines}')
    data = []
    modules = {'button':{'type':'button', 'targets': ['broadcaster'] }}
    for line in lines.split('\n'):
        print(f'line: {line}')
        module,targets = line.split(' -> ')
        moduleType=''
        if module[0] in ['%','&']:
            moduleType=module[0]
            module=module[1:]
        elif module == 'broadcaster':
            moduleType = 'broadcaster'
        modules[module] = {'type': moduleType, 'targets': targets.split(', ')}
        if modules[module]['type'] == '%':
            modules[module]['state'] = 'off'
        elif modules[module]['type'] == '&':
            modules[module]['inputs'] = {}
        if len(modules['button']['targets']) == 0:
            modules['button']['targets'].append(module)
    untyped_modules = []
    for module in modules.keys():
        for dst in modules[module]['targets']:
            if not dst in modules: # add untyped targets
                untyped_modules.append(dst)
            elif modules[dst]['type'] == '&': # they initially default to remembering a low pulse for each input.
                modules[dst]['inputs'][module] = 'low'
    for module in untyped_modules:
        #print(f'Untyped: {untyped_modules}')
        modules[module] = {'type':'untyped', 'targets': [] }
    for module in modules:
        for target in modules[module]['targets']:
            data.append((module,target))
    return data, modules



with open(sys.argv[1] , "r") as f:
    data,modules = parse_input(f.read())

G = nx.DiGraph()
G.add_edges_from(data)

# Choose a layout
pos = nx.spring_layout(G)  # You can try different layouts like circular_layout, shell_layout, spring_layout

# Prepare colors and shapes
colors = []
shapes = {'button': 's', 'broadcaster': '^', '%': 'o', '&': 'd'}  # Example: squares for buttons, triangles for broadcasters, etc.
node_shapes = []

for node in G.nodes():
    print(node)
    module_type = modules[node]['type']
    if module_type in shapes:
        node_shapes.append(shapes[module_type])
    else:
        node_shapes.append('o')  # default shape

    if module_type == '%':
        colors.append('red')
    elif module_type == '&':
        colors.append('green')
    else:
        colors.append('lightblue')

# Draw the graph
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=700, font_size=10, arrows=True)

# Show the plot
plt.show()