<template>
  <div class="bg-usuario">
    <div class="container py-4">
      <!-- Header -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Mis Tareas</h2>
        <button class="btn btn-danger" @click="logout">Cerrar sesión</button>
      </div>

      <!-- Layout principal: clima y tareas -->
      <div class="row g-3">
        <!-- Clima -->
        <div class="col-lg-3">
          <div class="card p-3 shadow-sm clima-contenedor">
            <h5 class="mb-3">Clima actual</h5>
            <div class="d-flex align-items-center justify-content-start gap-3">
              <div style="font-size: 2rem;">{{ clima.icono }}</div>
              <div>
                <p class="mb-1"><strong>Ciudad:</strong> {{ ciudad }}</p>
                <p class="mb-1"><strong>Temp:</strong> {{ clima.temperatura }} °C</p>
                <p class="mb-1"><strong>Condición:</strong> {{ clima.descripcion }}</p>
                <p class="mb-0"><strong>Viento:</strong> {{ clima.viento }} km/h</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tareas -->
        <div class="col-lg-9">
          <div class="card p-3 shadow-sm tareas-lista" v-if="tareas.length > 0">
            <h5 class="mb-3">Tareas Pendientes</h5>
            <div v-for="t in tareas" :key="t.id"
                 class="task-card mb-2 p-3 rounded d-flex justify-content-between align-items-center"
                 :class="t.completada ? 'completada' : 'pendiente'">

              <div class="flex-fill">
                <strong>{{ t.titulo }}</strong>
                <p class="m-0">{{ t.descripcion }}</p>
              </div>

              <div>
                <button class="btn btn-success" v-if="!t.completada" @click="marcarCompletada(t.id)">
                  Completar
                </button>
                <span v-else class="badge bg-success">Completada</span>
              </div>

            </div>
          </div>

          <div v-else class="alert alert-info">
            No tienes tareas asignadas.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import apiTareas from "@/apiTareas";
import axios from "axios";

export default {
  data() {
    return {
      tareas: [],
      usuarioId: null,
      rol: null,
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

  async mounted() {
    const token = localStorage.getItem("token");
    if (!token) return this.$router.push("/");

    const payload = JSON.parse(atob(token.split(".")[1]));
    this.usuarioId = payload.id_usuario;
    this.rol = payload.rol;

    if (this.rol === "admin") {
      this.$router.push("/dashboard-admin");
    } else {
      await this.cargarTareas();
      await this.obtenerClima();
    }
  },

  methods: {
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/");
    },

    async cargarTareas() {
      try {
        const token = localStorage.getItem("token");
        const res = await apiTareas.get("/tareas", { headers: { Authorization: "Bearer " + token } });
        this.tareas = res.data.tareas.filter(t => t.usuario_id === this.usuarioId);
      } catch (err) {
        console.error("Error cargando tareas:", err);
      }
    },

    async marcarCompletada(id) {
      try {
        const token = localStorage.getItem("token");
        await apiTareas.put(`/tareas/${id}/completar`, {}, { headers: { Authorization: "Bearer " + token } });
        await this.cargarTareas();
      } catch (err) {
        console.error("Error completando tarea:", err);
      }
    },

    async obtenerClima() {
      try {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${this.lat}&longitude=${this.lon}&current_weather=true`;
        const res = await axios.get(url);
        const weather = res.data.current_weather;

        const weatherIcons = {
          0: "☀️", 1: "🌤️", 2: "☁️", 3: "🌧️",
          45: "🌫️", 48: "🌫️❄️", 51: "🌦️", 53: "🌦️",
          55: "🌦️", 61: "🌧️", 63: "🌧️", 65: "🌧️",
          71: "❄️", 73: "❄️", 75: "❄️", 80: "🌦️",
          81: "🌧️", 82: "🌧️", 95: "⛈️", 96: "⛈️❄️", 99: "⛈️❄️"
        };

        const weatherCodes = {
          0: "Despejado", 1: "Parcialmente nublado", 2: "Nublado", 3: "Lluvia ligera",
          45: "Neblina", 48: "Neblina con escarcha", 51: "Llovizna ligera", 53: "Llovizna moderada",
          55: "Llovizna fuerte", 61: "Lluvia ligera", 63: "Lluvia moderada", 65: "Lluvia fuerte",
          71: "Nieve ligera", 73: "Nieve moderada", 75: "Nieve fuerte", 80: "Lluvia ligera con chubascos",
          81: "Lluvia moderada con chubascos", 82: "Lluvia fuerte con chubascos", 95: "Tormenta eléctrica",
          96: "Tormenta con granizo", 99: "Tormenta severa con granizo"
        };

        this.clima = {
          temperatura: weather.temperature,
          viento: weather.windspeed,
          descripcion: weatherCodes[weather.weathercode] || "Desconocido",
          icono: weatherIcons[weather.weathercode] || "❓"
        };
      } catch (err) {
        console.error("Error obteniendo clima:", err);
      }
    }
  }
};
</script>

<style scoped>
.bg-usuario {
  background: url("@/assets/blanco.jpg") no-repeat center center;
  background-size: cover;
  min-height: 100vh;
  padding: 2rem 0;
}

/* Cards */
.card { border-radius: 0.75rem; }

/* Scroll tareas */
.tareas-lista { max-height: 600px; overflow-y: auto; }

/* Tareas */
.task-card { transition: all 0.3s; border-left: 5px solid; }
.task-card.pendiente { border-color: #f0ad4e; background-color: #fff7e6; }
.task-card.completada { border-color: #5cb85c; background-color: #e6ffed; }

/* Clima */
.clima-contenedor { text-align: left; }

/* Botones */
.btn-success { 
  border-radius: 0.75rem; 
  background-color: #6c63ff;
  border: 3px solid black; /* Agrega borde negro */
}

.btn-success:hover {
  background-color: #3a3dff; /* verde un poco más oscuro */
  border: 3px solid black;
}

</style>
