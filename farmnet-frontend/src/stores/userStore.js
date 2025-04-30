import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUserStore = defineStore('user', () => {
  const user = ref(null);
  const token = ref(null);

  const isAuthenticated = computed(() => !!token.value); 
  const isAdmin = computed(() => user.value?.role === 'ADMIN'); 
  const isFarmer = computed(() => user.value?.role === 'FARMER'); 
  const isBuyer = computed(() => user.value?.role === 'BUYER'); /
  const isAgriExpert = computed(() => user.value?.role === 'AGRI_EXPERT'); //
  const currentUser = computed(() => user.value); // Get the current user

  // Login function
  function login(authToken, userData) {
    token.value = authToken;
    // Normalize the role to uppercase before storing it
    userData.role = userData.role.toUpperCase();
    user.value = userData;
    localStorage.setItem('token', authToken);
    localStorage.setItem('user', JSON.stringify(userData));
  }

  // Logout function
  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  // Initialize user from localStorage
  function initialize() {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    if (storedToken && storedUser) {
      token.value = storedToken;
      try {
        user.value = JSON.parse(storedUser);
        user.value.role = user.value.role.toUpperCase();
      } catch (e) {
        logout(); 
      }
    }
  }

  // Clear user data
  function clearUser() {
    logout();
  }

  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    isFarmer,
    isBuyer,
    isAgriExpert,
    currentUser,
    login,
    logout,
    initialize,
    clearUser,
  };
});
