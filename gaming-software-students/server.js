const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const flash = require('connect-flash');
const path = require('path');
const { sequelize } = require('./models');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

app.use(session({
  secret: 'gaming-software-students-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 24 * 60 * 60 * 1000 } // 24 hours
}));

app.use(flash());

// View engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Routes
const authRoutes = require('./routes/auth');
const studentRoutes = require('./routes/student');
const teacherRoutes = require('./routes/teacher');
const parentRoutes = require('./routes/parent');

app.use('/', authRoutes);
app.use('/student', studentRoutes);
app.use('/teacher', teacherRoutes);
app.use('/parent', parentRoutes);

// Home route
app.get('/', (req, res) => {
  if (req.session && req.session.userId) {
    if (req.session.role === 'student') {
      return res.redirect('/student/dashboard');
    } else if (req.session.role === 'teacher') {
      return res.redirect('/teacher/dashboard');
    } else if (req.session.role === 'parent') {
      return res.redirect('/parent/dashboard');
    }
  }
  res.redirect('/login');
});

// Initialize database and start server
sequelize.sync().then(() => {
  console.log('Database synced successfully');
  app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
  });
}).catch(err => {
  console.error('Unable to sync database:', err);
});
