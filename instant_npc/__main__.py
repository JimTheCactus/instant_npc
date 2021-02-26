import json

from .instant_npc import make_npc

def main():
    print(json.dumps(make_npc(), indent=2))

if __name__=="__main__":
    main()