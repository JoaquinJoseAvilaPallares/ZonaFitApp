from flask import Flask, render_template, url_for
from werkzeug.utils import redirect

from cliente import Cliente
from cliente_dao import ClienteDAO
from cliente_form import ClienteForm

app = Flask(__name__)

titulo_app = 'Zona Fit (GYM)'

app.config['SECRET_KEY'] = 'llave_secreta'

@app.route('/')
@app.route('/index.html')
def inicio():
    app.logger.debug('Entramos al path de inicio /')
    # Recuperamos los clientes de la base de datos
    clientes_db = ClienteDAO.seleccionar()

    # Creamos un objeto de cliente vacio
    cliente = Cliente()
    cliente_forma = ClienteForm(obj=cliente)
    return render_template('index.html', titulo=titulo_app,
                           clientes=clientes_db, forma=cliente_forma)

@app.route('/guardar', methods=['POST'])
def guardar():
    # Creamos los objetos vacios de cliente
    cliente = Cliente()
    cliente_forma = ClienteForm(obj=cliente)
    if cliente_forma.validate_on_submit():
        # Llenamos el objeto cliente con ls valores del formulario
        cliente_forma.populate_obj(cliente)
        if not cliente.id: # si el id es cadena vacia regresa verdadero
            # Guardamos el nuevo cliente en la base de datos
            ClienteDAO.insertar(cliente)
        else:
            ClienteDAO.actualizar(cliente)
        # Redireccionar a la pagina de inicio
        return redirect(url_for('inicio'))

@app.route('/editar/<int:id>')
def editar(id):
    cliente = ClienteDAO.seleccionar_por_id(id)
    cliente_forma = ClienteForm(obj=cliente)
    clientes_db = ClienteDAO.seleccionar()
    return render_template('index.html', titulo=titulo_app,
                           clientes=clientes_db,
                           forma=cliente_forma)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    cliente = Cliente(id=id)
    ClienteDAO.eliminar(cliente)
    return redirect(url_for('inicio'))

@app.route('/limpiar')
def limpiar():
    return redirect(url_for('inicio'))


if __name__ == '__main__':
    app.run(debug=True)