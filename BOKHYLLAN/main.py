#detta är för att starta programmet
from website import create_app

app = create_app()

if __name__ =='__main__':
    app.run(debug=True)