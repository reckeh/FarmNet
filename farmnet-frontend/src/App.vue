<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/market-prices">Market Prices</router-link>
      <router-link to="/profile" v-if="userStore.isAuthenticated">Profile</router-link>
      <router-link to="/admin-dashboard" v-if="userStore.isAdmin">Admin</router-link>
      <router-link to="/login" v-if="!userStore.isAuthenticated">Login</router-link>
      <router-link to="/register" v-if="!userStore.isAuthenticated">Register</router-link>
      <button v-if="userStore.isAuthenticated" @click="logout">Logout</button>
    </nav>

    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/userStore';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const userStore = useUserStore();
    const router = useRouter();

    onMounted(() => {
      userStore.initialize(); // Restore session if available
    });

    const logout = () => {
      userStore.logout();
      router.push('/login');
    };

    return {
      userStore,
      logout
    };
  }
};
</script>

<style scoped>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  min-height: 100vh;
  background-color: #f9f9f9;
}

nav {
  background: #ffffff;
  padding: 1rem;
  border-bottom: 1px solid #ddd;
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: flex-start;
}

nav a {
  color: #555;
  text-decoration: none;
  padding: 0.5rem 0.75rem;
  border-radius: 5px;
  transition: background-color 0.2s ease;
}

nav a.router-link-exact-active {
  background-color: #42b983;
  color: white;
  font-weight: bold;
}

nav a:hover {
  background-color: #e8f5e9;
}

button {
  border: none;
  background-color: transparent;
  cursor: pointer;
  padding: 0.5rem 0.75rem;
  color: #555;
  border-radius: 5px;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #ffeaea;
  color: #c0392b;
}

main {
  padding: 2rem;
}
</style>
