# This is not part of the module, it is only here for testing
# This and the settings.json file makes a simple python IDE

import guimakerp as gmp

def main() -> None:
    app: gmp.Application = gmp.Application()
    
    settings: dict = app.create_settings()
    print(settings)
    del settings
    
    app.create_window()
    
    app.place_widgets()
    
    app.run()
    del app

if __name__ == "__main__":
    main()
    del main