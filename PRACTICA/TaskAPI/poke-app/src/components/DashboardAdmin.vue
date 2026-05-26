<template>
  <div class="bg-admin vh-100 py-4">
    <div class="container">

      <!-- HEADER -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold">Panel Administrador</h2>

        <div class="d-flex gap-2">
          <router-link
            to="/dashboard-analisis"
            class="btn btn-success"
          >
            Ver Estadísticas
          </router-link>

          <button class="btn btn-danger" @click="logout">
            Cerrar sesión
          </button>
        </div>
      </div>

      <!-- CONTENIDO -->
      <div class="row g-3">

        <!-- IZQUIERDA -->
        <div class="col-lg-3 d-flex flex-column gap-3">

          <!-- CLIMA -->
          <div class="card p-3 shadow-sm">
            <h5 class="mb-3">Clima actual</h5>

            <div class="d-flex align-items-center gap-3">
              <div style="font-size: 2rem;">
                {{ clima.icono }}
              </div>

              <div>
                <p class="mb-1"><strong>Ciudad:</strong> {{ ciudad }}</p>
                <p class="mb-1"><strong>Temperatura:</strong> {{ clima.temperatura }} °C</p>
                <p class="mb-1"><strong>Condición:</strong> {{ clima.descripcion }}</p>
                <p class="mb-0"><strong>Viento:</strong> {{ clima.viento }} km/h</p>
              </div>
            </div>
          </div>

          <!-- CREAR TAREA -->
          <div class="card p-3 shadow-sm">
            <h5 class="mb-3">Crear / Asignar Tarea</h5>

            <div class="mb-2">
              <label>Usuario</label>

              <select v-model="usuarioSeleccionado" class="form-control">
                <option disabled value="">Seleccione un usuario</option>

                <option
                  v-for="u in usuariosFiltrados"
                  :key="u.id"
                  :value="u.id"
                >
                  {{ u.nombre }} ({{ u.email }}) - Chat ID: {{ u.chat_id || "N/A" }}
                </option>
              </select>
            </div>

            <div class="mb-2">
              <label>Título</label>
              <input v-model="titulo" class="form-control" />
            </div>

            <div class="mb-2">
              <label>Descripción</label>
              <textarea v-model="descripcion" class="form-control"></textarea>
            </div>

            <div class="mb-2">
              <label>Intervalo (min)</label>
              <input v-model.number="intervalo" type="number" class="form-control" min="1" />
            </div>

            <button class="btn btn-primary w-100" @click="crearTarea">
              Asignar
            </button>
          </div>
        </div>

        <!-- CENTRO -->
        <div class="col-lg-5">
          <div class="card p-3 shadow-sm tareas-lista">
            <h5 class="mb-3">Tareas</h5>

            <div
              v-for="t in tareas"
              :key="t.id"
              class="task-card mb-2 p-3 rounded d-flex justify-content-between align-items-start"
              :class="t.completada ? 'completada' : 'pendiente'"
            >
              <div>
                <strong>{{ t.titulo }}</strong>
                <p class="m-0">{{ t.descripcion }}</p>

                <small class="text-muted">
                  Asignada a: {{ obtenerNombreUsuario(t.usuario_id) }} |
                  Intervalo: {{ t.intervalo_notificacion }} min
                </small>
              </div>

              <span class="badge" :class="t.completada ? 'bg-success' : 'bg-warning'">
                {{ t.completada ? 'Completada' : 'Pendiente' }}
              </span>
            </div>

          </div>
        </div>

        <!-- DERECHA -->
        <div class="col-lg-4">
          <div class="card p-3 shadow-sm usuarios-lista">
            <h5 class="mb-3">Usuarios</h5>

            <div v-for="u in usuarios" :key="u.id" class="user-card mb-2 p-2 rounded">
              <strong>{{ u.nombre }}</strong>
              <p class="mb-0">{{ u.email }}</p>

              <small class="text-muted">
                {{ u.rol }} | Chat ID: {{ u.chat_id || "N/A" }}
              </small>
            </div>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import apiTareas from "@/apiTareas";
import apiUsuarios from "@/apiUsuarios";
import axios from "axios";

export default {
  name: "DashboardAdmin",

  data() {
    return {
      usuarios: [],
      tareas: [],

      usuarioSeleccionado: "",
      titulo: "",
      descripcion: "",
      intervalo: 60,

      ciudad: "Popayán",

      clima: {
        temperatura: null,
        viento: null,
        descripcion: "",
        icono: ""
      },

      lat: 2.4447,
      lon: -76.6146
    };
  },

  computed: {
    usuariosFiltrados() {
      return this.usuarios.filter(u => u.rol !== "admin");
    }
  },

  async mounted() {
    const token = localStorage.getItem("token");

    if (!token) return this.$router.push("/");

    const payload = JSON.parse(atob(token.split(".")[1]));

    if (payload.rol !== "admin") {
      return this.$router.push("/dashboard-user");
    }

    await this.cargarUsuarios();
    await this.cargarTareas();
    await this.obtenerClima();
  },

  methods: {

    logout() {
      localStorage.removeItem("token");
      this.$router.push("/");
    },

    obtenerNombreUsuario(id) {
      const u = this.usuarios.find(u => u.id === id);
      return u ? u.nombre : "Usuario desconocido";
    },

    async cargarUsuarios() {
      try {
        const token = localStorage.getItem("token");

        const res = await apiUsuarios.get("/usuarios", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        this.usuarios = res.data.usuarios;

      } catch (err) {
        console.error(err);
      }
    },

    async cargarTareas() {
      try {
        const token = localStorage.getItem("token");

        const res = await apiTareas.get("/tareas", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        this.tareas = res.data.tareas;

      } catch (err) {
        console.error(err);
      }
    },

    async crearTarea() {
      try {
        const token = localStorage.getItem("token");

        await apiTareas.post("/tareas", {
          usuario_id: parseInt(this.usuarioSeleccionado),
          titulo: this.titulo,
          descripcion: this.descripcion,
          intervalo_notificacion: this.intervalo
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        this.titulo = "";
        this.descripcion = "";
        this.usuarioSeleccionado = "";
        this.intervalo = 60;

        await this.cargarTareas();

      } catch (err) {
        alert(err.response?.data?.error || "Error creando tarea");
      }
    },

    async obtenerClima() {
      try {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${this.lat}&longitude=${this.lon}&current_weather=true`;

        const res = await axios.get(url);
        const weather = res.data.current_weather;

        this.clima = {
          temperatura: weather.temperature,
          viento: weather.windspeed,
          descripcion: "Actualizado",
          
        };

      } catch (err) {
        console.error(err);
      }
    }
  }
};
</script>

<style scoped>
.bg-admin {
  background: #eef2f7;
  font-family: 'Segoe UI', sans-serif;
}

/* CARDS GENERALES */
.card {
  border: none;
  border-radius: 14px;
  background: #ffffff;
}

/* LISTA DE TAREAS */
.tareas-lista {
  max-height: 560px;
  overflow-y: auto;
}

.task-card {
  border-left: 5px solid transparent;
  transition: transform 0.15s;
}
.task-card:hover {
  transform: translateX(3px);
}
.task-card.completada {
  background: #f0fdf4;
  border-left-color: #22c55e;
}
.task-card.pendiente {
  background: #fffbeb;
  border-left-color: #f59e0b;
}

/* LISTA DE USUARIOS */
.usuarios-lista {
  max-height: 560px;
  overflow-y: auto;
}

.user-card {
  background: #f8fafc;
  border-left: 4px solid #3b82f6;
  transition: background 0.15s;
}
.user-card:hover {
  background: #eff6ff;
}

/* FORMULARIO */
.form-control {
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  font-size: 0.9rem;
}
.form-control:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
}

label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 3px;
}

/* BOTONES */
.btn-primary {
  background: #2563eb;
  border: none;
  border-radius: 8px;
  font-weight: 600;
}
.btn-primary:hover {
  background: #1d4ed8;
}
.btn-success {
  border-radius: 8px;
  font-weight: 600;
}
.btn-danger {
  border-radius: 8px;
  font-weight: 600;
}

/* TÍTULO */
h2 {
  color: #1e3a5f;
  font-size: 1.5rem;
}

h5 {
  color: #334155;
  font-size: 1rem;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 8px;
}

/* BADGES */
.badge {
  font-size: 0.75rem;
  padding: 5px 10px;
  border-radius: 20px;
}

/* CLIMA */
.card p {
  font-size: 0.85rem;
  color: #475569;
}

/* SCROLLBAR */
.tareas-lista::-webkit-scrollbar,
.usuarios-lista::-webkit-scrollbar {
  width: 5px;
}
.tareas-lista::-webkit-scrollbar-thumb,
.usuarios-lista::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
</style>