const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Fee = sequelize.define('Fee', {
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
  academicYear: {
    type: DataTypes.STRING,
    allowNull: false
  },
  amount: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false
  },
  isPaid: {
    type: DataTypes.BOOLEAN,
    defaultValue: false
  },
  paidDate: {
    type: DataTypes.DATE,
    allowNull: true
  }
});

module.exports = Fee;
