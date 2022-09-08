from website import create_app

#Create new app -> 'app'
app = create_app()

if __name__ == '__main__':
        app.run(debug=True)