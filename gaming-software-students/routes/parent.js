const express = require('express');
const router = express.Router();
const PDFDocument = require('pdfkit');
const { User, Attempt, Quiz, Feedback, Fee } = require('../models');
const { isAuthenticated, isParent } = require('../middleware/auth');

router.use(isAuthenticated);
router.use(isParent);

// Dashboard
router.get('/dashboard', async (req, res) => {
  try {
    const parent = await User.findByPk(req.session.userId, {
      include: [{ model: User, as: 'children' }]
    });

    let children = parent.children || [];
    
    // If no children linked, find students with this parent's ID
    if (children.length === 0) {
      children = await User.findAll({
        where: { parentId: req.session.userId }
      });
    }

    res.render('parent/dashboard', {
      user: req.session,
      children
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// View Child Profile
router.get('/child/:id', async (req, res) => {
  try {
    const child = await User.findByPk(req.params.id);
    
    // Verify this child belongs to this parent
    if (child.parentId !== req.session.userId) {
      return res.status(403).send('Access denied');
    }

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

    const fees = await Fee.findAll({
      where: { studentId: req.params.id },
      order: [['academicYear', 'DESC']]
    });

    const hasDue = fees.some(fee => !fee.isPaid);

    res.render('parent/child-detail', {
      user: req.session,
      child,
      attempts,
      feedbacks,
      fees,
      hasDue
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Download Report Card
router.get('/child/:id/report/:year', async (req, res) => {
  try {
    const child = await User.findByPk(req.params.id);
    
    if (child.parentId !== req.session.userId) {
      return res.status(403).send('Access denied');
    }

    const attempts = await Attempt.findAll({
      where: { studentId: req.params.id },
      include: [{ model: Quiz, as: 'quiz' }]
    });

    const doc = new PDFDocument();
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `attachment; filename=report-card-${child.name}-${req.params.year}.pdf`);
    
    doc.pipe(res);

    // Header
    doc.fontSize(20).text('Academic Report Card', { align: 'center' });
    doc.moveDown();
    doc.fontSize(12).text(`Student Name: ${child.name}`);
    doc.text(`Standard: ${child.standard}`);
    doc.text(`Section: ${child.section}`);
    doc.text(`School: ${child.school}`);
    doc.text(`Academic Year: ${req.params.year}`);
    doc.moveDown();

    // Quiz Results
    doc.fontSize(16).text('Quiz Results', { underline: true });
    doc.moveDown();

    if (attempts.length === 0) {
      doc.fontSize(12).text('No quiz attempts found for this academic year.');
    } else {
      attempts.forEach((attempt, index) => {
        doc.fontSize(12).text(`${index + 1}. ${attempt.quiz.title} (${attempt.quiz.subject})`);
        doc.text(`   Score: ${attempt.score}/${attempt.totalMarks}`);
        doc.text(`   Date: ${new Date(attempt.completedAt).toLocaleDateString()}`);
        doc.moveDown(0.5);
      });
    }

    doc.end();
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

module.exports = router;
