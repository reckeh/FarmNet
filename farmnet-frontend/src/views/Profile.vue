<template>
  <div class="profile-container">
    <h2>User Profile</h2>

    <form @submit.prevent="updateProfile">
      <div>
        <label>Username:</label>
        <input type="text" v-model="form.username" required />
      </div>

      <div>
        <label>Email:</label>
        <input type="email" v-model="form.email" required />
      </div>

      <div>
        <label>Password:</label>
        <input type="password" v-model="form.password" placeholder="Leave blank to keep current password" />
      </div>

      <button type="submit">Update Profile</button>
    </form>

    <div v-if="message" class="message">{{ message }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Profile',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: ''
      },
      message: ''
    };
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/users/profile', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        const user = res.data;
        this.form.username = user.username;
        this.form.email = user.email;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async updateProfile() {
      try {
        const res = await axios.put('http://127.0.0.1:5000/users/profile', this.form, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.message = res.data.message;
        this.form.password = ''; // Clear password field after update
      } catch (error) {
        console.error('Error updating profile:', error);
        this.message = error.response?.data?.error || 'Update failed.';
      }
    }
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 12px;
}
input {
  width: 100%;
  padding: 8px;
  margin: 8px 0 16px;
  border-radius: 4px;
  border: 1px solid #ccc;
}
button {
  padding: 10px 20px;
  background-color: #006400;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  background-color: #008000;
}
.message {
  margin-top: 20px;
  color: green;
}
</style>
