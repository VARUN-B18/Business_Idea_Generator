const express = require('express');
const router = express.Router();
const { User, Quiz, Question, Attempt, Feedback, Fee } = require('../models');
const { isAuthenticated, isStudent } = require('../middleware/auth');
const { Op } = require('sequelize');

router.use(isAuthenticated);
router.use(isStudent);

// Dashboard
router.get('/dashboard', async (req, res) => {
  try {
    const student = await User.findByPk(req.session.userId);
    const quizzes = await Quiz.findAll({
      where: {
        standard: student.standard,
        isActive: true
      },
      include: [{ model: Question, as: 'questions' }]
    });

    const attempts = await Attempt.findAll({
      where: { studentId: req.session.userId },
      include: [{ model: Quiz, as: 'quiz' }]
    });

    const attemptedQuizIds = attempts.map(a => a.quizId);
    const availableQuizzes = quizzes.filter(q => !attemptedQuizIds.includes(q.id));

    res.render('student/dashboard', {
      user: req.session,
      student,
      quizzes: availableQuizzes,
      attempts
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Profile
router.get('/profile', async (req, res) => {
  try {
    const student = await User.findByPk(req.session.userId);
    res.render('student/profile', {
      user: req.session,
      student
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Take Quiz
router.get('/quiz/:id', async (req, res) => {
  try {
    const quiz = await Quiz.findByPk(req.params.id, {
      include: [{ model: Question, as: 'questions' }]
    });

    if (!quiz) {
      return res.status(404).send('Quiz not found');
    }

    const existingAttempt = await Attempt.findOne({
      where: {
        studentId: req.session.userId,
        quizId: quiz.id
      }
    });

    if (existingAttempt) {
      return res.redirect('/student/results');
    }

    res.render('student/take-quiz', {
      user: req.session,
      quiz
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Submit Quiz
router.post('/quiz/:id/submit', async (req, res) => {
  try {
    const quiz = await Quiz.findByPk(req.params.id, {
      include: [{ model: Question, as: 'questions' }]
    });

    const answers = req.body;
    let score = 0;
    let totalMarks = 0;

    quiz.questions.forEach(question => {
      totalMarks += question.marks;
      if (answers[`question_${question.id}`] === question.correctAnswer) {
        score += question.marks;
      }
    });

    await Attempt.create({
      studentId: req.session.userId,
      quizId: quiz.id,
      answers,
      score,
      totalMarks,
      isGraded: true
    });

    res.redirect('/student/results');
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Results
router.get('/results', async (req, res) => {
  try {
    const attempts = await Attempt.findAll({
      where: { studentId: req.session.userId },
      include: [{ model: Quiz, as: 'quiz' }],
      order: [['completedAt', 'DESC']]
    });

    res.render('student/results', {
      user: req.session,
      attempts
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Leaderboard
router.get('/leaderboard', async (req, res) => {
  try {
    const student = await User.findByPk(req.session.userId);
    
    const attempts = await Attempt.findAll({
      where: { isGraded: true },
      include: [
        { 
          model: User, 
          as: 'student',
          where: { standard: student.standard }
        },
        { model: Quiz, as: 'quiz' }
      ]
    });

    const studentScores = {};
    attempts.forEach(attempt => {
      const studentId = attempt.studentId;
      if (!studentScores[studentId]) {
        studentScores[studentId] = {
          name: attempt.student.name,
          totalScore: 0,
          totalAttempts: 0
        };
      }
      studentScores[studentId].totalScore += attempt.score;
      studentScores[studentId].totalAttempts += 1;
    });

    const leaderboard = Object.values(studentScores)
      .sort((a, b) => b.totalScore - a.totalScore);

    res.render('student/leaderboard', {
      user: req.session,
      leaderboard
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Feedback
router.get('/feedback', async (req, res) => {
  try {
    const feedbacks = await Feedback.findAll({
      where: { studentId: req.session.userId },
      include: [{ model: User, as: 'teacher' }],
      order: [['createdAt', 'DESC']]
    });

    res.render('student/feedback', {
      user: req.session,
      feedbacks
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Fees
router.get('/fees', async (req, res) => {
  try {
    const fees = await Fee.findAll({
      where: { studentId: req.session.userId },
      order: [['academicYear', 'DESC']]
    });

    const hasDue = fees.some(fee => !fee.isPaid);

    res.render('student/fees', {
      user: req.session,
      fees,
      hasDue
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

module.exports = router;
