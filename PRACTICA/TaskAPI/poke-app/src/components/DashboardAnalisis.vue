<template>
  <div class="analisis-bg min-vh-100 py-4">
    <div class="container">

      <!-- HEADER -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 class="fw-bold mb-0 titulo-principal"> Panel de Análisis</h2>
        </div>
        <router-link to="/dashboard-admin" class="btn btn-outline-secondary">
          ← Volver
        </router-link>
      </div>

      <!-- LOADING -->
      <div v-if="cargando" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-2 text-muted">Cargando métricas...</p>
      </div>

      <!-- ERROR -->
      <div v-if="error" class="alert alert-danger">
         {{ error }}
      </div>

      <div v-if="!cargando">

        <!-- TARJETAS RESUMEN -->
        <div class="row g-3 mb-4">
          <div class="col-6 col-md-3">
            <div class="card-metrica card-total">
              <div class="metrica-icono"></div>
              <div class="metrica-valor">{{ metricas.total_tareas }}</div>
              <div class="metrica-label">Total Tareas</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="card-metrica card-completadas">
              <div class="metrica-icono"></div>
              <div class="metrica-valor">{{ metricas.tareas_completadas }}</div>
              <div class="metrica-label">Pendientes</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="card-metrica card-pendientes">
              <div class="metrica-icono"></div>
              <div class="metrica-valor">{{ metricas.tareas_pendientes }}</div>
              <div class="metrica-label">Completadas</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="card-metrica card-porcentaje">
              <div class="metrica-icono"></div>
              <div class="metrica-valor">{{ metricas.porcentaje_completado }}%</div>
              <div class="metrica-label">Completado</div>
            </div>
          </div>
        </div>

        <!-- BARRA DE PROGRESO GENERAL -->
        <div class="card p-3 mb-4 shadow-sm">
          <h6 class="fw-bold mb-2">Progreso general</h6>
          <div class="progress" style="height: 24px; border-radius: 12px;">
            <div
              class="progress-bar bg-success"
              :style="{ width: metricas.porcentaje_completado + '%' }"
              role="progressbar"
            >
              {{ metricas.porcentaje_completado }}%
            </div>
          </div>
        </div>

        <div class="row g-3">

          <!-- PRODUCTIVIDAD POR USUARIO -->
          <div class="col-md-6">
            <div class="card p-3 shadow-sm h-100">
              <h6 class="fw-bold mb-3"> Productividad por usuario</h6>

              <div
                v-for="(datos, nombre) in productividad"
                :key="nombre"
                class="mb-3"
              >
                <div class="d-flex justify-content-between mb-1">
                  <span class="fw-semibold">{{ nombre }}</span>
                  <span class="badge bg-primary">{{ datos.tareas_completadas }}/{{ datos.tareas_totales }}</span>
                </div>
                <div class="progress" style="height: 14px; border-radius: 8px;">
                  <div
                    class="progress-bar"
                    :class="datos.porcentaje >= 75 ? 'bg-success' : datos.porcentaje >= 40 ? 'bg-warning' : 'bg-danger'"
                    :style="{ width: datos.porcentaje + '%' }"
                  >
                    {{ datos.porcentaje }}%
                  </div>
                </div>
              </div>

              <p v-if="!Object.keys(productividad).length" class="text-muted small">Sin datos</p>
            </div>
          </div>

          <!-- TIEMPO PROMEDIO -->
          <div class="col-md-6">
            <div class="card p-3 shadow-sm h-100">
              <h6 class="fw-bold mb-3"> Tiempo promedio de completado</h6>

              <div class="text-center py-3" v-if="tiempoPromedio.dias !== undefined">
                <div class="tiempo-dias">{{ tiempoPromedio.dias }}</div>
                <div class="text-muted">días en promedio</div>
                <div class="mt-2 text-secondary small">
                  ≈ {{ tiempoPromedio.horas }} horas
                </div>
                <div class="mt-3">
                  <span class="badge bg-info text-dark">
                    {{ tiempoPromedio.total_tareas_analizadas }} tareas analizadas
                  </span>
                </div>
              </div>

              <p v-else class="text-muted small">Sin datos de tiempo</p>
            </div>
          </div>

        

            
        

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiAnalisis from "@/apiAnalisis";

export default {
  name: "DashboardAnalisis",

  data() {
    return {
      cargando: true,
      error: null,
      fechaConsulta: "",

      metricas: {
        total_tareas: 0,
        tareas_completadas: 0,
        tareas_pendientes: 0,
        porcentaje_completado: 0
      },

      productividad: {},

      tiempoPromedio: {},

      metricasDiarias: {}
    };
  },

  async mounted() {
    const token = localStorage.getItem("token");
    if (!token) return this.$router.push("/");

    await this.cargarDatos();
  },

  methods: {

    async cargarDatos() {
      this.cargando = true;
      this.error = null;

      try {
        const [dashboard, productividad, metricas, tiempo] = await Promise.all([
          apiAnalisis.get("/analisis/dashboard"),
          apiAnalisis.get("/analisis/productividad"),
          apiAnalisis.get("/analisis/metricas"),
          apiAnalisis.get("/analisis/tiempo")
        ]);

        const d = dashboard.data;
        this.metricas = d.metricas_generales || {};
        this.fechaConsulta = d.fecha_consulta
          ? new Date(d.fecha_consulta).toLocaleString("es-CO")
          : "";

        this.productividad = productividad.data.productividad_por_usuario || {};

        this.metricasDiarias = metricas.data.tareas_completadas_por_dia || {};

        this.tiempoPromedio = tiempo.data.tiempo_promedio_completado || {};

      } catch (err) {
        this.error = "No se pudo conectar con el servicio de análisis. Verifica que esté activo.";
        console.error(err);
      } finally {
        this.cargando = false;
      }
    },

    formatearFecha(fecha) {
      const d = new Date(fecha + "T00:00:00");
      return d.toLocaleDateString("es-CO", { day: "2-digit", month: "2-digit" });
    }
  }
};
</script>

<style scoped>
.analisis-bg {
  background: #f0f4f8;
  font-family: 'Segoe UI', sans-serif;
}

.titulo-principal {
  color: #1a237e;
}

/* TARJETAS MÉTRICAS */
.card-metrica {
  border-radius: 16px;
  padding: 20px 16px;
  text-align: center;
  color: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}
.card-metrica:hover { transform: translateY(-3px); }

.card-total      { background: linear-gradient(135deg, #1565c0, #1565c0); }
.card-completadas{ background: linear-gradient(135deg, #1565c0, #1565c0); }
.card-pendientes { background: linear-gradient(135deg, #1565c0, #1565c0); }
.card-porcentaje { background: linear-gradient(135deg, #1565c0, #1565c0); }

.metrica-icono { font-size: 1.8rem; margin-bottom: 6px; }
.metrica-valor { font-size: 2rem; font-weight: 800; line-height: 1; }
.metrica-label { font-size: 0.8rem; opacity: 0.9; margin-top: 4px; }

/* TIEMPO PROMEDIO */
.tiempo-dias {
  font-size: 3.5rem;
  font-weight: 900;
  color: #1565c0;
  line-height: 1;
}

/* BARRAS DIARIAS */
.metricas-barras {
  height: 140px;
  align-items: flex-end;
}
.barra-dia {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.barra-relleno {
  width: 100%;
  border-radius: 6px 6px 0 0;
  min-height: 4px;
  transition: height 0.5s ease;
}
.barra-cantidad {
  font-size: 0.75rem;
  font-weight: 700;
  margin-top: 2px;
  color: #333;
}
.barra-fecha {
  font-size: 0.65rem;
  color: #1565c0;
}
</style>
