const sequelize = require('../config/database');
const User = require('./User');
const Quiz = require('./Quiz');
const Question = require('./Question');
const Attempt = require('./Attempt');
const Feedback = require('./Feedback');
const Fee = require('./Fee');

// Define associations
User.hasMany(Quiz, { foreignKey: 'teacherId', as: 'createdQuizzes' });
Quiz.belongsTo(User, { foreignKey: 'teacherId', as: 'teacher' });

Quiz.hasMany(Question, { foreignKey: 'quizId', as: 'questions', onDelete: 'CASCADE' });
Question.belongsTo(Quiz, { foreignKey: 'quizId' });

User.hasMany(Attempt, { foreignKey: 'studentId', as: 'attempts' });
Attempt.belongsTo(User, { foreignKey: 'studentId', as: 'student' });

Quiz.hasMany(Attempt, { foreignKey: 'quizId', as: 'attempts' });
Attempt.belongsTo(Quiz, { foreignKey: 'quizId', as: 'quiz' });

User.hasMany(Feedback, { foreignKey: 'studentId', as: 'receivedFeedback' });
Feedback.belongsTo(User, { foreignKey: 'studentId', as: 'student' });

User.hasMany(Feedback, { foreignKey: 'teacherId', as: 'givenFeedback' });
Feedback.belongsTo(User, { foreignKey: 'teacherId', as: 'teacher' });

User.hasMany(Fee, { foreignKey: 'studentId', as: 'fees' });
Fee.belongsTo(User, { foreignKey: 'studentId', as: 'student' });

// Parent-child relationship
User.hasMany(User, { foreignKey: 'parentId', as: 'children' });
User.belongsTo(User, { foreignKey: 'parentId', as: 'parent' });

module.exports = {
  sequelize,
  User,
  Quiz,
  Question,
  Attempt,
  Feedback,
  Fee
};
