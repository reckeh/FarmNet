<template>
  <div :style="containerStyle">
    <h2 :style="titleStyle">🔐 Login</h2>
    <form @submit.prevent="handleLogin" :style="formStyle">
      <input
        type="email"
        placeholder="Email"
        v-model="email"
        required
        :style="inputStyle"
      />
      <input
        type="password"
        placeholder="Password"
        v-model="password"
        required
        :style="inputStyle"
      />
      <button type="submit" :style="buttonStyle">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
      <p v-if="error" :style="errorStyle">{{ error }}</p>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      loading: false,
      containerStyle: {
        maxWidth: '400px',
        margin: '100px auto',
        padding: '30px',
        border: '1px solid #ccc',
        borderRadius: '10px',
        backgroundColor: '#f9f9f9',
        fontFamily: 'Arial, sans-serif',
      },
      titleStyle: {
        textAlign: 'center',
        marginBottom: '20px',
      },
      formStyle: {
        display: 'flex',
        flexDirection: 'column',
        gap: '15px',
      },
      inputStyle: {
        padding: '10px',
        fontSize: '16px',
        borderRadius: '5px',
        border: '1px solid #ccc',
      },
      buttonStyle: {
        padding: '10px',
        fontSize: '16px',
        backgroundColor: '#4CAF50',
        color: '#fff',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
      },
      errorStyle: {
        color: 'red',
        textAlign: 'center',
      },
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = '';

      try {
        const response = await fetch('http://localhost:5000/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Login failed');
        }

        // Save token and user data
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));

        // Redirect based on user role
        const role = data.user?.role;
        const dashboards = {
          farmer: '/farmer/dashboard',
          buyer: '/buyer/dashboard',
          admin: '/admin/dashboard',
        };

        const redirectPath = dashboards[role] || '/';
        this.$router.push(redirectPath);
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
