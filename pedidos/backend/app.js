const express = require('express');
const mysql = require('mysql');

const app = express();
app.use(express.json());

function conectarDB() {
  const db = mysql.createConnection({
    host: 'db',
    user: 'user',
    password: 'password',
    database: 'domicilios'
  });

  db.connect(err => {
    if (err) {
      console.log(' Esperando MySQL...');
      setTimeout(conectarDB, 2000);
    } else {
      console.log(' Conectado a MySQL');

      // Crear tabla si no existe
      db.query(`
        CREATE TABLE IF NOT EXISTS pedidos (
          id INT AUTO_INCREMENT PRIMARY KEY,
          nombre VARCHAR(100)
        )
      `);

      // Ruta para guardar datos
      app.post('/api/pedidos', (req, res) => {
        const { nombre } = req.body;

        db.query(
          'INSERT INTO pedidos (nombre) VALUES (?)',
          [nombre],
          (err, result) => {
            if (err) {
              res.status(500).send('Error al guardar');
            } else {
              res.send('Pedido guardado ');
            }
          }
        );
      });
// EDITAR pedido
app.put('/api/pedidos/:id', (req, res) => {
  const { nombre } = req.body;
  const { id } = req.params;

  db.query(
    'UPDATE pedidos SET nombre = ? WHERE id = ?',
    [nombre, id],
    (err, result) => {
      if (err) {
        res.status(500).send('Error al actualizar');
      } else {
        res.send('Pedido actualizado ✏️');
      }
    }
  );
});

//  ELIMINAR pedido
app.delete('/api/pedidos/:id', (req, res) => {
  const { id } = req.params;

  db.query(
    'DELETE FROM pedidos WHERE id = ?',
    [id],
    (err, result) => {
      if (err) {
        res.status(500).send('Error al eliminar');
      } else {
        res.send('Pedido eliminado ');
      }
    }
  );
});
      // Ruta para consultar datos
      app.get('/api/pedidos', (req, res) => {
        db.query('SELECT * FROM pedidos', (err, results) => {
          if (err) {
            res.status(500).send('Error');
          } else {
            res.json(results);
          }
        });
      });

      app.listen(3000, () => {
        console.log('Servidor en puerto 3000');
      });
    }
  });
}

conectarDB();