with open('data/adresy.txt', 'r') as f:
    links = f.readlines()
    for link in range(len(links)):
        links[link] = links[link].replace('\n', '')

print(links)
