import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUserStore = defineStore('user', () => {
  // State variables for user and token
  const user = ref(null);
  const token = ref(null);

  // Computed properties to check if the user is authenticated and their role
  const isAuthenticated = computed(() => !!token.value); // If token exists, user is authenticated
  const isAdmin = computed(() => user.value?.role === 'ADMIN'); // Admin role check
  const isFarmer = computed(() => user.value?.role === 'FARMER'); // Farmer role check
  const isBuyer = computed(() => user.value?.role === 'BUYER'); // Buyer role check
  const isAgriExpert = computed(() => user.value?.role === 'AGRI_EXPERT'); // AgriExpert role check
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
        // Ensure the role is in uppercase when initializing
        user.value.role = user.value.role.toUpperCase();
      } catch (e) {
        logout(); // If there is an error in parsing, logout
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
