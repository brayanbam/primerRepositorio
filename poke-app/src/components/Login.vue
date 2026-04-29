<template>
  <div class="vh-100 d-flex align-items-center justify-content-center bg-login">
    <div class="row w-85 shadow-lg rounded-4 overflow-hidden" style="max-width: 1700px;">

      <!-- Imagen -->
      <div class="col-8 d-none d-md-block p-0">
        <img
          src="@/assets/login-illustration.png"
          alt="Login illustration"
          class="img-fluid h-100 w-100 object-cover"
        />
      </div>

      <!-- Formulario -->
      <div class="col-12 col-md-4 d-flex align-items-center justify-content-center">
        <div class="p-5 rounded-4 shadow-sm" style="width: 85%; max-width: 450px; background-color: #ffffff;">
          <h3 class="text-dark fw-bold mb-4 text-center">Bienvenido de nuevo</h3>

          <form @submit.prevent="login">
            <div class="mb-3">
              <label class="form-label">Correo electrónico</label>
              <input
                v-model="email"
                type="email"
                class="form-control"
                required
                placeholder="usuario@correo.com"
              />
            </div>

            <div class="mb-4">
              <label class="form-label">Contraseña</label>
              <input
                v-model="password"
                type="password"
                class="form-control"
                required
                placeholder="••••••••"
              />
            </div>

            <button type="submit" class="btn btn-primary w-100 py-2 fw-semibold">
              Iniciar sesión
            </button>

            <p v-if="error" class="text-danger mt-3 text-center">{{ error }}</p>
          </form>

          <button
            class="btn-invertido w-100 py-2 fw-semibold mt-3"
            @click="$router.push('/crear-usuario')"
          >
            Crear usuario
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiUsuarios from "@/apiUsuarios";

export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
      error: "",
    };
  },

  methods: {
    async login() {
      try {
        const res = await apiUsuarios.post("/login", {
          email: this.email,
          password: this.password,
        });

        const token = res.data.token;
        localStorage.setItem("token", token);
        const payload = JSON.parse(atob(token.split(".")[1]));

        if (payload.rol === "admin") {
          this.$router.push("/dashboard-admin");
        } else {
          this.$router.push("/dashboard-user");
        }
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          this.error = err.response.data.error;
        } else {
          this.error = "Error en el servidor.";
        }
      }
    },
  },
};
</script>

<style scoped>
.bg-login {
  background: url("@/assets/blanco.jpg") no-repeat center center;
  background-size: cover;
}
.rounded-4 { border-radius: 1rem; }
.shadow-lg { box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); }
.object-cover { object-fit: cover; }
.form-control { border-radius: 0.75rem; padding: 0.75rem; }
.btn-primary { background-color: #6c63ff; border: none; border-radius: 0.75rem; transition: all 0.3s ease; }
.btn-primary:hover { background-color: #3a3dff; transform: translateY(-2px); }
.btn-primary:active { transform: translateY(0); }
.w-85 { width: 85% !important; }
.btn-invertido { border: 2px solid #6c63ff; background-color: #ffffff; color: #6c63ff; border-radius: 0.75rem; padding: 0.75rem; transition: all 0.3s ease; cursor: pointer; }
.btn-invertido:hover { background-color: #2e2d3d; color: #ffffff; transform: translateY(-2px); }
.btn-invertido:active { transform: translateY(0); }
</style>
