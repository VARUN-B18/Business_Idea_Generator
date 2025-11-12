const express = require('express');
const router = express.Router();
const { User } = require('../models');

router.get('/login', (req, res) => {
  res.render('login', { 
    error: req.flash('error'),
    success: req.flash('success')
  });
});

router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ where: { email } });

    if (!user) {
      req.flash('error', 'Invalid email or password');
      return res.redirect('/login');
    }

    const isValid = await user.validPassword(password);
    if (!isValid) {
      req.flash('error', 'Invalid email or password');
      return res.redirect('/login');
    }

    req.session.userId = user.id;
    req.session.role = user.role;
    req.session.name = user.name;

    // Redirect based on role
    if (user.role === 'student') {
      res.redirect('/student/dashboard');
    } else if (user.role === 'teacher') {
      res.redirect('/teacher/dashboard');
    } else if (user.role === 'parent') {
      res.redirect('/parent/dashboard');
    }
  } catch (error) {
    console.error(error);
    req.flash('error', 'An error occurred during login');
    res.redirect('/login');
  }
});

router.get('/register', (req, res) => {
  res.render('register', { 
    error: req.flash('error'),
    success: req.flash('success')
  });
});

router.post('/register', async (req, res) => {
  try {
    const { name, email, password, role, standard, section, school } = req.body;

    const existingUser = await User.findOne({ where: { email } });
    if (existingUser) {
      req.flash('error', 'Email already registered');
      return res.redirect('/register');
    }

    await User.create({
      name,
      email,
      password,
      role,
      standard: role === 'student' ? standard : null,
      section: role === 'student' ? section : null,
      school
    });

    req.flash('success', 'Registration successful! Please log in.');
    res.redirect('/login');
  } catch (error) {
    console.error(error);
    req.flash('error', 'An error occurred during registration');
    res.redirect('/register');
  }
});

router.get('/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/login');
});

module.exports = router;
