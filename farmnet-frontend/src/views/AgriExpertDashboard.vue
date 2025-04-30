<template>
    <div :style="containerStyle">
      <h2 :style="headerStyle">Welcome, {{ expertName }}</h2>
  
      <!-- Navigation Links -->
      <div :style="navStyle">
        <button :style="navButtonStyle" @click="currentView = 'articles'">My Articles</button>
        <button :style="navButtonStyle" @click="currentView = 'questions'">Answer Questions</button>
        <button :style="logoutStyle" @click="logout">Logout</button>
      </div>
  
      <!-- Articles Section -->
      <div v-if="currentView === 'articles'" :style="sectionStyle">
        <h3 :style="subHeaderStyle">My Articles</h3>
        <form @submit.prevent="submitArticle" :style="formStyle">
          <input v-model="newArticle.title" placeholder="Title" :style="inputStyle" required />
          <textarea v-model="newArticle.content" placeholder="Content" :style="textareaStyle" required></textarea>
          <button :style="submitButtonStyle">Publish</button>
        </form>
  
        <ul>
          <li v-for="article in articles" :key="article.id" :style="listItemStyle">
            <strong>{{ article.title }}</strong><br />
            <span>{{ article.content }}</span>
          </li>
        </ul>
      </div>
  
      <!-- Questions Section -->
      <div v-else-if="currentView === 'questions'" :style="sectionStyle">
        <h3 :style="subHeaderStyle">Questions from Farmers</h3>
        <div v-for="question in questions" :key="question.id" :style="questionCardStyle">
          <p><strong>Q:</strong> {{ question.question_text }}</p>
          
          <div v-if="question.answer" :style="answerStyle">
            <span><strong>A:</strong> {{ question.answer }}</span>
          </div>
  
          <div v-else>
            <input v-model="question.reply" placeholder="Your answer..." :style="inputStyle" />
            <button @click="submitAnswer(question)" :style="submitButtonStyle">Reply</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        expertName: 'Agri Expert',
        currentView: 'articles',
        articles: [],
        newArticle: {
          title: '',
          content: ''
        },
        questions: []
      };
    },
    methods: {
      async fetchArticles() {
        try {
          const response = await axios.get('http://localhost:5000/api/expert/articles');
          this.articles = response.data;
        } catch (error) {
          console.error('Failed to load articles:', error);
        }
      },
      async fetchQuestions() {
        try {
          const response = await axios.get('http://localhost:5000/api/expert/questions');
          this.questions = response.data.map(q => ({ ...q, reply: '' }));
        } catch (error) {
          console.error('Failed to load questions:', error);
        }
      },
      async submitArticle() {
        try {
          const response = await axios.post('http://localhost:5000/api/expert/articles', this.newArticle);
          this.articles.push(response.data);
          this.newArticle.title = '';
          this.newArticle.content = '';
        } catch (error) {
          console.error('Failed to submit article:', error);
        }
      },
      async submitAnswer(question) {
        try {
          const payload = {
            question_id: question.id,
            answer_text: question.reply
          };
          const response = await axios.post('http://localhost:5000/api/expert/answers', payload);
          question.answer = response.data.answer_text;
          question.reply = '';
        } catch (error) {
          console.error('Failed to submit answer:', error);
        }
      },
      logout() {
        alert("Logging out...");
        window.location.href = "/login";
      }
    },
    mounted() {
      this.fetchArticles();
      this.fetchQuestions();
    },
    computed: {
      containerStyle() {
        return {
          maxWidth: '900px',
          margin: '30px auto',
          padding: '20px',
          border: '1px solid #ddd',
          borderRadius: '12px',
          backgroundColor: '#fff',
          boxShadow: '0 2px 12px rgba(0,0,0,0.1)',
          fontFamily: 'Arial, sans-serif'
        };
      },
      headerStyle() {
        return {
          fontSize: '26px',
          marginBottom: '20px',
          textAlign: 'center'
        };
      },
      navStyle() {
        return {
          display: 'flex',
          justifyContent: 'space-around',
          marginBottom: '25px'
        };
      },
      navButtonStyle() {
        return {
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: '#007BFF',
          color: '#fff',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer'
        };
      },
      logoutStyle() {
        return {
          ...this.navButtonStyle,
          backgroundColor: '#dc3545'
        };
      },
      sectionStyle() {
        return {
          marginTop: '20px'
        };
      },
      subHeaderStyle() {
        return {
          fontSize: '22px',
          marginBottom: '10px'
        };
      },
      formStyle() {
        return {
          display: 'flex',
          flexDirection: 'column',
          gap: '10px',
          marginBottom: '20px'
        };
      },
      inputStyle() {
        return {
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '6px'
        };
      },
      textareaStyle() {
        return {
          height: '80px',
          ...this.inputStyle
        };
      },
      submitButtonStyle() {
        return {
          padding: '10px',
          backgroundColor: '#28a745',
          color: '#fff',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer'
        };
      },
      listItemStyle() {
        return {
          padding: '10px',
          borderBottom: '1px solid #eee'
        };
      },
      questionCardStyle() {
        return {
          marginBottom: '20px',
          padding: '15px',
          border: '1px solid #ddd',
          borderRadius: '8px',
          backgroundColor: '#f9f9f9'
        };
      },
      answerStyle() {
        return {
          marginTop: '10px',
          color: '#28a745',
          fontWeight: 'bold'
        };
      }
    }
  };
  </script>
  