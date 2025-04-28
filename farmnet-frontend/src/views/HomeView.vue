<template>
  <div class="home" style="font-family: 'Arial', sans-serif; background-color: #f7f7f7; color: #333;">
    <!-- Hero Section -->
    <section class="hero-section" style="text-align: center; padding: 40px 20px; background-color: #3f9d2f; color: white;">
      <h1 style="font-size: 2.5rem; margin-bottom: 20px;">Welcome to FarmNet</h1>
      <p style="font-size: 1.2rem; margin-bottom: 30px;">Your partner in sustainable farming for a smart future</p>

      <!-- Auth Buttons -->
      <div v-if="!isAuthenticated" style="display: flex; justify-content: center; gap: 20px;">
        <router-link to="/login" class="button login-btn" style="background-color: #ff7f50; padding: 12px 20px; border-radius: 5px; color: white; text-decoration: none; font-size: 1rem;">Login</router-link>
        <router-link to="/register" class="button register-btn" style="background-color: #32cd32; padding: 12px 20px; border-radius: 5px; color: white; text-decoration: none; font-size: 1rem;">Register</router-link>
      </div>
      <div v-else>
        <p style="font-size: 1.2rem;">Hello, {{ currentUser.name }}</p>

        <!-- Profile Button -->
        <router-link to="/profile" class="button profile-btn" style="background-color: #6f42c1; padding: 12px 24px; margin: 12px; color: white; text-decoration: none; border-radius: 5px;">My Profile</router-link>

        <!-- Role-based Dashboards -->
        <div v-if="isFarmer" class="dashboard-links">
          <router-link to="/farmer-dashboard" class="button dashboard-btn" style="background-color: #3f9d2f; padding: 12px 24px; border-radius: 5px; color: white; text-decoration: none;">Farmer Dashboard</router-link>
        </div>
        <div v-if="isBuyer" class="dashboard-links">
          <router-link to="/buyer-dashboard" class="button dashboard-btn" style="background-color: #32cd32; padding: 12px 24px; border-radius: 5px; color: white; text-decoration: none;">Buyer Dashboard</router-link>
        </div>
        <div v-if="isAdmin" class="dashboard-links">
          <router-link to="/admin-dashboard" class="button dashboard-btn" style="background-color: #ff7f50; padding: 12px 24px; border-radius: 5px; color: white; text-decoration: none;">Admin Dashboard</router-link>
        </div>
        <div v-if="isAgriExpert" class="dashboard-links">
          <router-link to="/expert-dashboard" class="button dashboard-btn" style="background-color: #ff6347; padding: 12px 24px; border-radius: 5px; color: white; text-decoration: none;">AgriExpert Dashboard</router-link>
        </div>

        <button @click="logout" class="logout-btn" style="background-color: #dc3545; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1rem; margin-top: 20px;">Logout</button>
      </div>
    </section>

    <!-- Weather Section -->
    <section class="weather-container" style="margin: 2rem auto; max-width: 600px; padding: 20px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
      <div class="weather-card" style="text-align: center;">
        <h2 class="title" style="font-size: 1.5rem; margin-bottom: 1rem;">Current Weather</h2>
        <div v-if="loading" class="loading" style="font-size: 1rem; color: #888;">Loading weather data...</div>
        <div v-else-if="error" class="error" style="font-size: 1rem; color: #e74c3c;">{{ error }}</div>
        <div v-else class="weather-info" style="font-size: 1rem; color: #333;">
          <div class="location" style="font-weight: bold; margin-bottom: 10px;">{{ weather.location }}</div>
          <img :src="iconUrl" alt="Weather Icon" class="icon" style="width: 100px; margin-bottom: 10px;" />
          <div class="temperature" style="font-size: 2rem; margin-bottom: 10px;">
            {{ isFahrenheit ? convertToFahrenheit(weather.temperature) : weather.temperature }}°
            {{ isFahrenheit ? 'F' : 'C' }}
          </div>
          <div class="details" style="font-size: 1rem;">
            <p><strong>Condition:</strong> {{ weather.weather }}</p>
            <p><strong>Humidity:</strong> {{ weather.humidity }}%</p>
            <p><strong>Wind Speed:</strong> {{ weather.wind_speed }} m/s</p>
            <p><strong>Recorded At:</strong> {{ weather.date }}</p>
          </div>

          <!-- Weather Refresh Button -->
          <button @click="detectLocation" class="weather-refresh-btn" style="background-color: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1rem; margin-top: 20px;">Refresh Weather</button>
        </div>
      </div>
    </section>

    <!-- Other Sections (Smart Farming, Featured Products, Testimonials, Footer) -->
    <!-- Add your other sections here styled inline similarly -->
  </div>
</template>

<script>
import { useUserStore } from '../stores/userStore';
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'HomeView',
  setup() {
    const userStore = useUserStore();
    const router = useRouter();

    const isAuthenticated = computed(() => userStore.isAuthenticated);
    const isFarmer = computed(() => userStore.currentUser?.role === 'FARMER');
    const isBuyer = computed(() => userStore.currentUser?.role === 'BUYER');
    const isAdmin = computed(() => userStore.currentUser?.role === 'ADMIN');
    const isAgriExpert = computed(() => userStore.currentUser?.role === 'AGRI_EXPERT');
    const currentUser = computed(() => userStore.currentUser);

    const logout = () => {
      userStore.logout();
      router.push('/login');
    };

    // Weather Logic
    const weather = ref({});
    const loading = ref(true);
    const error = ref('');
    const isFahrenheit = ref(false);

    const iconUrl = computed(() =>
      weather.value.icon ? `https://openweathermap.org/img/wn/${weather.value.icon}@2x.png` : ''
    );

    const convertToFahrenheit = (celsius) => ((celsius * 9) / 5 + 32).toFixed(1);

    const getWeather = async (lat, lon) => {
      loading.value = true;
      error.value = '';
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://127.0.0.1:5000/weather/weather?lat=${lat}&lon=${lon}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        weather.value = response.data;
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load weather data.';
      } finally {
        loading.value = false;
      }
    };

    const detectLocation = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const lat = position.coords.latitude.toFixed(4);
            const lon = position.coords.longitude.toFixed(4);
            getWeather(lat, lon);
          },
          () => {
            error.value = 'Failed to get geolocation. Try refreshing.';
            loading.value = false;
          }
        );
      } else {
        error.value = 'Geolocation is not supported by your browser.';
        loading.value = false;
      }
    };

    onMounted(() => {
      userStore.initialize();
      detectLocation();
    });

    return {
      isAuthenticated,
      isFarmer,
      isBuyer,
      isAdmin,
      isAgriExpert,
      currentUser,
      logout,
      weather,
      loading,
      error,
      isFahrenheit,
      convertToFahrenheit,
      iconUrl,
      detectLocation,
    };
  },
};
</script>
