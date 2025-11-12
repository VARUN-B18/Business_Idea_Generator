const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Attempt = sequelize.define('Attempt', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  studentId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: 'Users',
      key: 'id'
    }
  },
  quizId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: 'Quizzes',
      key: 'id'
    }
  },
  answers: {
    type: DataTypes.TEXT,
    allowNull: false,
    get() {
      const rawValue = this.getDataValue('answers');
      return rawValue ? JSON.parse(rawValue) : {};
    },
    set(value) {
      this.setDataValue('answers', JSON.stringify(value));
    }
  },
  score: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  totalMarks: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  isGraded: {
    type: DataTypes.BOOLEAN,
    defaultValue: false
  },
  completedAt: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW
  }
});

module.exports = Attempt;
