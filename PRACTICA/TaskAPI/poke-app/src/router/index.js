import { createRouter, createWebHashHistory } from 'vue-router'
import Login from '../components/Login.vue'
import DashboardUsuario from '../components/DashboardUsuario.vue'
import DashboardAdmin from '../components/DashboardAdmin.vue'
import CrearUsuario from '../components/CrearUsuario.vue'
import DashboardAnalisis from '../components/DashboardAnalisis.vue'

const routes = [
  { path: '/', name: 'Login', component: Login },

  {
    path: '/dashboard-user',
    name: 'DashboardUsuario',
    component: DashboardUsuario,
    meta: { requiereAuth: true, rol: 'usuario' }
  },

  {
    path: '/dashboard-admin',
    name: 'DashboardAdmin',
    component: DashboardAdmin,
    meta: { requiereAuth: true, rol: 'admin' }
  },

  {
    path: '/crear-usuario',
    name: 'CrearUsuario',
    component: CrearUsuario
  },

  {
    path: '/dashboard-analisis',
    name: 'DashboardAnalisis',
    component: DashboardAnalisis,
    meta: { requiereAuth: true, rol: 'admin' }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {

  const token = localStorage.getItem('token')

  if (!token && to.meta.requiereAuth) {
    return next('/')
  }

  if (token) {

    const payload =
      JSON.parse(atob(token.split('.')[1]))

    const rol = payload.rol

    if (to.meta.rol && to.meta.rol !== rol) {
      return next('/')
    }
  }

  next()
})

export default router