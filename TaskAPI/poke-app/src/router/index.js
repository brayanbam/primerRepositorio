import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import DashboardUsuario from '../components/DashboardUsuario.vue'
import DashboardAdmin from '../components/DashboardAdmin.vue'
import CrearUsuario from '../components/CrearUsuario.vue'

const routes = [
  { path: '/', name: 'Login', component: Login },

  {
    path: '/dashboard-user',   // ruta en minúsculas para usuarios
    name: 'DashboardUsuario',
    component: DashboardUsuario,
    meta: { requiereAuth: true, rol: 'usuario' }
  },

  {
    path: '/dashboard-admin',  // ruta en minúsculas para admin
    name: 'DashboardAdmin',
    component: DashboardAdmin,
    meta: { requiereAuth: true, rol: 'admin' }
  },

  {
    path: '/crear-usuario',
    name: 'CrearUsuario',
    component: CrearUsuario  
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (!token && to.meta.requiereAuth) {
    return next('/')
  }

  if (token) {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const rol = payload.rol

    if (to.meta.rol && to.meta.rol !== rol) {
      return next('/') 
    }
  }

  next()
})

export default router
