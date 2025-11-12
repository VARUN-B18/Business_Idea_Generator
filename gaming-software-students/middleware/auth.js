const isAuthenticated = (req, res, next) => {
  if (req.session && req.session.userId) {
    return next();
  }
  req.flash('error', 'Please log in to access this page');
  res.redirect('/login');
};

const isStudent = (req, res, next) => {
  if (req.session && req.session.role === 'student') {
    return next();
  }
  res.status(403).send('Access denied');
};

const isTeacher = (req, res, next) => {
  if (req.session && req.session.role === 'teacher') {
    return next();
  }
  res.status(403).send('Access denied');
};

const isParent = (req, res, next) => {
  if (req.session && req.session.role === 'parent') {
    return next();
  }
  res.status(403).send('Access denied');
};

module.exports = {
  isAuthenticated,
  isStudent,
  isTeacher,
  isParent
};
