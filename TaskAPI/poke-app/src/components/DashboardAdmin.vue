<template>
  <div class="bg-admin min-vh-100 py-4">
    <div class="container">

      <!-- Header -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Panel Administrador</h2>
        <div class="d-flex gap-2">
          <button
            class="btn btn-info"
            @click="mostrarAnaliticas = !mostrarAnaliticas"
          >
           📊 Analíticas
          </button>
          <button
            class="btn btn-danger"
           @click="logout"
          >
            Cerrar sesión
          </button>
        </div>
      </div>
      <!-- ANALÍTICAS -->
<div
  v-if="mostrarAnaliticas"
  class="card p-4 shadow-sm mb-4"
>

  <h4 class="mb-4">
    📊 Analíticas del Sistema
  </h4>

  <div class="row text-center">

    <div class="col-md-3">
      <div class="metric-card">
        <h3>{{ metricas.total_tareas }}</h3>
        <p>Total tareas</p>
      </div>
    </div>

    <div class="col-md-3">
      <div class="metric-card">
        <h3>{{ metricas.tareas_completadas }}</h3>
        <p>Completadas</p>
      </div>
    </div>

    <div class="col-md-3">
      <div class="metric-card">
        <h3>{{ metricas.tareas_pendientes }}</h3>
        <p>Pendientes</p>
      </div>
    </div>

    <div class="col-md-3">
      <div class="metric-card">
        <h3>{{ metricas.porcentaje_completado }}%</h3>
        <p>Productividad</p>
      </div>
    </div>

  </div>

</div>
      <!-- Layout principal: tres columnas -->
      <div class="row g-3">
        <!-- Columna izquierda: Clima + Crear tarea -->
        <div class="col-lg-3 d-flex flex-column gap-3">
          <!-- Clima actual -->
          <div class="card p-3 shadow-sm">
            <h5 class="mb-3">Clima actual</h5>
            <div class="d-flex align-items-center justify-content-start gap-3">
              <div style="font-size: 2rem;">{{ clima.icono }}</div>
              <div>
                <p class="mb-1"><strong>Ciudad:</strong> {{ ciudad }}</p>
                <p class="mb-1"><strong>Temperatura:</strong> {{ clima.temperatura }} °C</p>
                <p class="mb-1"><strong>Condición:</strong> {{ clima.descripcion }}</p>
                <p class="mb-0"><strong>Viento:</strong> {{ clima.viento }} km/h</p>
              </div>
            </div>
          </div>

          <!-- Crear/Asignar tarea -->
          <div class="card p-3 shadow-sm">
            <h5 class="mb-3">Crear / Asignar Tarea</h5>
            <div class="mb-2">
              <label>Usuario</label>
              <select v-model="usuarioSeleccionado" class="form-control">
                <option disabled value="">Seleccione un usuario</option>
                <option v-for="u in usuariosFiltrados" :key="u.id" :value="u.id">
                  {{ u.nombre }} ({{ u.email }}) - Chat ID: {{ u.chat_id || "N/A" }}
                </option>
              </select>
            </div>
            <div class="mb-2">
              <label>Título</label>
              <input v-model="titulo" class="form-control" placeholder="Título de la tarea"/>
            </div>
            <div class="mb-2">
              <label>Descripción</label>
              <textarea v-model="descripcion" class="form-control" placeholder="Descripción"></textarea>
            </div>
            <div class="mb-2">
              <label>Intervalo (min)</label>
              <input v-model.number="intervalo" type="number" class="form-control" min="1"/>
            </div>
            <button class="btn btn-primary w-100" @click="crearTarea">Asignar</button>
          </div>
        </div>

        <!-- Columna central: Lista de tareas -->
        <div class="col-lg-5">
          <div class="card p-3 shadow-sm tareas-lista">
            <h5 class="mb-3">Tareas</h5>
            <div v-for="t in tareas" :key="t.id" class="task-card mb-2 p-3 rounded d-flex justify-content-between align-items-start"
                 :class="t.completada ? 'completada' : 'pendiente'">
              <div>
                <strong>{{ t.titulo }}</strong>
                <p class="m-0">{{ t.descripcion }}</p>
                <small class="text-muted">
                  Asignada a: {{ obtenerNombreUsuario(t.usuario_id) }} | Intervalo: {{ t.intervalo_notificacion }} min
                </small>
              </div>
              <span class="badge" :class="t.completada ? 'bg-success' : 'bg-warning'">
                {{ t.completada ? 'Completada' : 'Pendiente' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Columna derecha: Usuarios -->
        <div class="col-lg-4">
          <div class="card p-3 shadow-sm usuarios-lista">
            <h5 class="mb-3">Usuarios</h5>
            <div v-for="u in usuarios" :key="u.id" class="user-card mb-2 p-2 rounded">
              <strong>{{ u.nombre }}</strong>
              <p class="mb-0">{{ u.email }}</p>
              <small class="text-muted">{{ u.rol }} | Chat ID: {{ u.chat_id || "N/A" }}</small>
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
import apiAnalisis from "@/apiAnalisis";
import axios from "axios";

export default {
  data() {
  return {
    usuarios: [],
    tareas: [],

    mostrarAnaliticas: false,

    metricas: {
      total_tareas: 0,
      tareas_completadas: 0,
      tareas_pendientes: 0,
      porcentaje_completado: 0
    },
      usuarioSeleccionado: "",
      titulo: "",
      descripcion: "",
      intervalo: 60,
      ciudad: "Popayán",
      clima: { temperatura: null, viento: null, descripcion: "", icono: "" },
      lat: 2.4447,
      lon: -76.6146
    };
  },
  computed: {
    usuariosFiltrados() { return this.usuarios.filter(u => u.rol !== "admin"); }
  },
  async mounted() {

  const token = localStorage.getItem("token");

  if (!token) return this.$router.push("/");

  const payload = JSON.parse(
    atob(token.split(".")[1])
  );

  if (payload.rol !== "admin") {

    return this.$router.push("/dashboard-user");

  }

  await this.cargarUsuarios();

  await this.cargarTareas();

  await this.obtenerClima();

  await this.cargarMetricas();
},
  methods: {
    async cargarMetricas() {

  try {

    const res = await apiAnalisis.get("/analisis/dashboard");

    this.metricas = res.data.metricas_generales;

  } catch (err) {

    console.error(
      "Error cargando métricas:",
      err.response?.data || err
    );

  }
},
    logout() { localStorage.removeItem("token"); this.$router.push("/"); },
    obtenerNombreUsuario(id) { const u = this.usuarios.find(x => x.id === id); return u ? u.nombre : "Usuario desconocido"; },
    async cargarUsuarios() {
      try {
        const token = localStorage.getItem("token");
        const res = await apiUsuarios.get("/usuarios", { headers: { Authorization: `Bearer ${token}` } });
        this.usuarios = res.data.usuarios;
      } catch (err) { console.error("Error cargando usuarios:", err.response?.data || err); }
    },
    async cargarTareas() {
      try {
        const token = localStorage.getItem("token");
        const res = await apiTareas.get("/tareas", { headers: { Authorization: `Bearer ${token}` } });
        this.tareas = res.data.tareas;
      } catch (err) { console.error("Error cargando tareas:", err.response?.data || err); }
    },
    async crearTarea() {

  if (!this.usuarioSeleccionado || !this.titulo.trim()) {

    return alert(
      "Debe seleccionar un usuario y escribir un título."
    );

  }

  try {

    const token = localStorage.getItem("token");

    await apiTareas.post(
      "/tareas",
      {
        usuario_id: parseInt(this.usuarioSeleccionado),
        titulo: this.titulo,
        descripcion: this.descripcion,
        intervalo_notificacion: this.intervalo
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    this.titulo = "";
    this.descripcion = "";
    this.usuarioSeleccionado = "";
    this.intervalo = 60;

    // ACTUALIZAR TAREAS
    await this.cargarTareas();

    // ACTUALIZAR ANALÍTICAS
    await this.cargarMetricas();

  } catch (err) {

    console.error(
      "Error creando tarea:",
      err.response?.data || err
    );

    alert(
      err.response?.data?.error ||
      "Error creando la tarea"
    );
  }
},
    async obtenerClima() {
      try {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${this.lat}&longitude=${this.lon}&current_weather=true`;
        const res = await axios.get(url);
        const weather = res.data.current_weather;
        const weatherIcons = {0:"☀️",1:"🌤️",2:"☁️",3:"🌧️",45:"🌫️",48:"🌫️❄️",51:"🌦️",53:"🌦️",55:"🌦️",61:"🌧️",63:"🌧️",65:"🌧️",71:"❄️",73:"❄️",75:"❄️",80:"🌦️",81:"🌧️",82:"🌧️",95:"⛈️",96:"⛈️❄️",99:"⛈️❄️"};
        const weatherDescriptions = {0:"Despejado",1:"Parcialmente nublado",2:"Nublado",3:"Lluvia ligera",45:"Niebla",48:"Niebla con escarcha",51:"Llovizna ligera",53:"Llovizna moderada",55:"Llovizna densa",61:"Lluvia ligera",63:"Lluvia moderada",65:"Lluvia intensa",71:"Nieve ligera",73:"Nieve moderada",75:"Nieve intensa",80:"Chubascos ligeros",81:"Chubascos moderados",82:"Chubascos intensos",95:"Tormenta",96:"Tormenta con granizo",99:"Tormenta severa"};
        this.clima = { temperatura: weather.temperature, viento: weather.windspeed, descripcion: weatherDescriptions[weather.weathercode] || "Desconocido", icono: weatherIcons[weather.weathercode] || "❓" };
      } catch (err) { console.error("Error obteniendo clima:", err); }
    }
  }
};
</script>

<style scoped>
.bg-admin {
  background: url("@/assets/blanco.jpg") no-repeat center center;
  background-size: cover;
  min-height: 100vh;
  padding: 2rem 0;
}
.card { border-radius: 0.75rem; }
.tareas-lista, .usuarios-lista { max-height: 600px; overflow-y: auto; }
.task-card { transition: all 0.3s; border-left: 5px solid; }
.task-card.pendiente { border-color: #f0ad4e; background-color: #fff7e6; }
.task-card.completada { border-color: #5cb85c; background-color: #e6ffed; }
.user-card { background-color: #f8f9fa; transition: all 0.3s; }
.user-card:hover { background-color: #e2e6ea; }
.btn-primary { background-color: #6c63ff; border: none; border-radius: 0.75rem; }
.btn-primary:hover { background-color: #3a3dff; }

.metric-card {

  background: #f8f9fa;

  border-radius: 15px;

  padding: 20px;

  transition: 0.3s;
}

.metric-card:hover {

  transform: scale(1.03);

  background: #e9ecef;
}

.metric-card h3 {

  color: #6c63ff;

  font-weight: bold;
}
</style>
