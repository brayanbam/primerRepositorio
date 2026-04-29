<template>
  <div class="vh-100 d-flex align-items-center justify-content-center bg-gradient-to-right">

    <div class="p-5 rounded-4 shadow-lg bg-white" style="width: 90%; max-width: 450px;">

      <h3 class="text-dark fw-bold mb-4 text-center">Crear Nuevo Usuario</h3>

      <form @submit.prevent="crearUsuario">
        <div class="mb-3">
          <label class="form-label">Nombre</label>
          <input v-model="nombre" type="text" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Correo electrónico</label>
          <input v-model="email" type="email" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Contraseña</label>
          <input v-model="password" type="password" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Confirmar contraseña</label>
          <input v-model="password2" type="password" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Chat ID</label>
          <input v-model="chat_id" type="text" class="form-control" required />
        </div>

        <button type="submit" class="btn btn-primary w-100 py-2 fw-semibold">
          Crear Usuario
        </button>

        <router-link to="/" class="btn-invertido w-100 py-2 fw-semibold mt-3 text-center">
          Regresar al Login
        </router-link>

        <p v-if="mensaje" class="text-success mt-3 text-center">{{ mensaje }}</p>
        <p v-if="error" class="text-danger mt-3 text-center">{{ error }}</p>
      </form>

    </div>
  </div>
</template>

<script>
import apiUsuarios from "@/apiUsuarios";

export default {
  name: "CreateUser",

  data() {
    return {
      nombre: "",
      email: "",
      password: "",
      password2: "",
      chat_id: "",
      mensaje: "",
      error: "",
    };
  },

  methods: {
    async crearUsuario() {
      if (this.password !== this.password2) {
        this.error = "Las contraseñas no coinciden.";
        this.mensaje = "";
        return;
      }

      try {
        const res = await apiUsuarios.post("/usuarios", {
          nombre: this.nombre,
          email: this.email,
          password: this.password,
          chat_id: this.chat_id,
        }, {
          headers: { "Content-Type": "application/json" }
        });

        if (res.status === 201) {
          this.mensaje = "Usuario creado exitosamente.";
          this.error = "";

          this.nombre = "";
          this.email = "";
          this.password = "";
          this.password2 = "";
          this.chat_id = "";

          setTimeout(() => { this.$router.push("/"); }, 1000);
        }

      } catch (err) {
        this.mensaje = "";
        if (err.response && err.response.data && err.response.data.error) {
          this.error = err.response.data.error;
        } else {
          this.error = "No se pudo crear el usuario. Verifica si el email ya está registrado.";
        }
      }
    },
  },
};
</script>

<style scoped>
.bg-gradient-to-right {
  background: url("@/assets/blanco.jpg") no-repeat center center;
  background-size: cover;       /* La imagen cubre todo el contenedor */
  min-height: 100vh;            /* Ocupa toda la altura de la ventana */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
}

.form-control { border-radius: 0.75rem; padding: 0.75rem; }
.btn-primary { background-color: #6c63ff; border: none; border-radius: 0.75rem; transition: 0.3s ease; }
.btn-primary:hover { background-color: #3a3dff; transform: translateY(-2px); }
.btn-invertido { display: inline-block; border: 2px solid #6c63ff; background-color: #ffffff; color: #6c63ff; border-radius: 0.75rem; padding: 0.75rem; transition: 0.3s ease; text-decoration: none; }
.btn-invertido:hover { background-color: #2e2d3d; color: #ffffff; transform: translateY(-2px); }
</style>
