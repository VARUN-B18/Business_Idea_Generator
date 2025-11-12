const express = require('express');
const router = express.Router();
const { User, Quiz, Question, Attempt, Feedback } = require('../models');
const { isAuthenticated, isTeacher } = require('../middleware/auth');

router.use(isAuthenticated);
router.use(isTeacher);

// Dashboard
router.get('/dashboard', async (req, res) => {
  try {
    const quizzes = await Quiz.findAll({
      where: { teacherId: req.session.userId },
      include: [{ model: Question, as: 'questions' }]
    });

    const students = await User.findAll({
      where: { role: 'student' }
    });

    res.render('teacher/dashboard', {
      user: req.session,
      quizzes,
      studentCount: students.length
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Create Quiz - Form
router.get('/quiz/create', (req, res) => {
  res.render('teacher/create-quiz', {
    user: req.session
  });
});

// Create Quiz - Submit
router.post('/quiz/create', async (req, res) => {
  try {
    const { title, subject, standard, description, questions } = req.body;

    const quiz = await Quiz.create({
      title,
      subject,
      standard,
      description,
      teacherId: req.session.userId
    });

    // Parse questions (assuming they come as arrays)
    const questionCount = Array.isArray(questions) ? questions.length : 1;
    
    for (let i = 0; i < questionCount; i++) {
      const prefix = Array.isArray(questions) ? `questions[${i}]` : 'questions';
      await Question.create({
        quizId: quiz.id,
        questionText: req.body[`${prefix}[questionText]`] || req.body['questionText'],
        optionA: req.body[`${prefix}[optionA]`] || req.body['optionA'],
        optionB: req.body[`${prefix}[optionB]`] || req.body['optionB'],
        optionC: req.body[`${prefix}[optionC]`] || req.body['optionC'],
        optionD: req.body[`${prefix}[optionD]`] || req.body['optionD'],
        correctAnswer: req.body[`${prefix}[correctAnswer]`] || req.body['correctAnswer'],
        marks: req.body[`${prefix}[marks]`] || req.body['marks'] || 1
      });
    }

    res.redirect('/teacher/dashboard');
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// View Students
router.get('/students', async (req, res) => {
  try {
    const students = await User.findAll({
      where: { role: 'student' },
      order: [['standard', 'ASC'], ['name', 'ASC']]
    });

    res.render('teacher/students', {
      user: req.session,
      students
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// View Student Activity
router.get('/student/:id', async (req, res) => {
  try {
    const student = await User.findByPk(req.params.id);
    const attempts = await Attempt.findAll({
      where: { studentId: req.params.id },
      include: [{ model: Quiz, as: 'quiz' }],
      order: [['completedAt', 'DESC']]
    });

    const feedbacks = await Feedback.findAll({
      where: { studentId: req.params.id },
      include: [{ model: User, as: 'teacher' }],
      order: [['createdAt', 'DESC']]
    });

    res.render('teacher/student-detail', {
      user: req.session,
      student,
      attempts,
      feedbacks
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Add Feedback
router.post('/feedback', async (req, res) => {
  try {
    const { studentId, subject, message } = req.body;

    await Feedback.create({
      teacherId: req.session.userId,
      studentId,
      subject,
      message
    });

    res.redirect(`/teacher/student/${studentId}`);
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// View Quiz Attempts
router.get('/quiz/:id/attempts', async (req, res) => {
  try {
    const quiz = await Quiz.findByPk(req.params.id);
    const attempts = await Attempt.findAll({
      where: { quizId: req.params.id },
      include: [{ model: User, as: 'student' }],
      order: [['completedAt', 'DESC']]
    });

    res.render('teacher/quiz-attempts', {
      user: req.session,
      quiz,
      attempts
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

module.exports = router;
