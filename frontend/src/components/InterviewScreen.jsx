import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, MessageSquare, User, Clock, TrendingUp } from 'lucide-react';
import { interviewAPI } from '../services/api';

const panelistInfo = {
  'hiring-manager': {
    name: 'Hiring Manager',
    role: 'Behavioral & Leadership',
    icon: '🎭',
    color: 'from-blue-500 to-cyan-500',
    bgColor: 'from-blue-50 to-cyan-50',
  },
  'system-architect': {
    name: 'System Architect',
    role: 'Design & Scalability',
    icon: '🏗️',
    color: 'from-purple-500 to-pink-500',
    bgColor: 'from-purple-50 to-pink-50',
  },
  'senior-dev': {
    name: 'Senior Developer',
    role: 'Technical Depth & Debugging',
    icon: '💻',
    color: 'from-orange-500 to-red-500',
    bgColor: 'from-orange-50 to-red-50',
  },
};

const InterviewScreen = ({ sessionData, onComplete }) => {
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState(sessionData.question);
  const [questionNumber, setQuestionNumber] = useState(sessionData.question_number);
  const [totalQuestions] = useState(sessionData.total_questions);
  const [currentPanelist, setCurrentPanelist] = useState(sessionData.current_panelist);

  const panelist = panelistInfo[currentPanelist] || panelistInfo['hiring-manager'];
  const progress = (questionNumber / totalQuestions) * 100;

  const wordCount = answer.trim().split(/\s+/).filter(Boolean).length;
  const charCount = answer.length;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!answer.trim()) {
      setError('Please provide an answer');
      return;
    }

    try {
      setLoading(true);
      setError('');
      const data = await interviewAPI.submitAnswer(sessionData.session_id, answer);

      if (data.completed) {
        onComplete(data.dashboard);
      } else {
        setCurrentQuestion(data.question);
        setQuestionNumber(data.question_number);
        setCurrentPanelist(data.current_panelist);
        setAnswer('');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to submit answer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div className="max-w-5xl mx-auto">
        {/* Progress Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-10"
        >
          <div className="flex justify-between items-center mb-4">
            <div className="flex items-center gap-3">
              <Clock className="w-6 h-6 text-slate-600" />
              <span className="text-lg font-bold text-slate-900">
                Question {questionNumber} of {totalQuestions}
              </span>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-md border border-slate-200">
              <TrendingUp className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-semibold text-slate-700">
                {Math.round(progress)}% Complete
              </span>
            </div>
          </div>
          <div className="h-4 bg-slate-200 rounded-full overflow-hidden shadow-inner">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="h-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-full shadow-lg"
            />
          </div>
        </motion.div>

        {/* Panelist Card */}
        <motion.div
          key={currentPanelist}
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-3xl shadow-xl p-8 mb-8 border-2 border-slate-100"
        >
          <div className="flex items-center gap-6">
            <motion.div
              initial={{ rotate: -10 }}
              animate={{ rotate: 0 }}
              transition={{ type: "spring", stiffness: 200 }}
              className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${panelist.color} flex items-center justify-center text-4xl shadow-xl`}
            >
              {panelist.icon}
            </motion.div>
            <div>
              <h3 className="text-2xl font-bold text-slate-900 mb-1">{panelist.name}</h3>
              <p className="text-lg text-slate-600 font-medium">{panelist.role}</p>
            </div>
          </div>
        </motion.div>

        {/* Question Card */}
        <motion.div
          key={currentQuestion}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className={`bg-gradient-to-br ${panelist.bgColor} rounded-3xl shadow-xl p-10 mb-8 border-2 border-slate-100`}
        >
          <div className="flex items-start gap-4">
            <div className={`w-12 h-12 bg-gradient-to-br ${panelist.color} rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg`}>
              <MessageSquare className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h4 className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-3">Question</h4>
              <p className="text-xl text-slate-900 leading-relaxed font-medium whitespace-pre-wrap">
                {currentQuestion}
              </p>
            </div>
          </div>
        </motion.div>

        {/* Answer Form */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="bg-white rounded-3xl shadow-xl p-10 border-2 border-slate-100"
        >
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-8 p-5 bg-red-50 border-2 border-red-200 rounded-2xl text-red-700 font-medium"
            >
              {error}
            </motion.div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label className="flex items-center gap-3 text-xl font-bold text-slate-900 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                  <User className="w-5 h-5 text-white" />
                </div>
                Your Answer
              </label>
              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Type your answer here... Be specific and provide concrete examples with measurable outcomes."
                rows={10}
                className="w-full px-6 py-4 border-2 border-slate-200 rounded-2xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all outline-none resize-none text-slate-700 text-lg"
                required
                disabled={loading}
              />
              <div className="mt-4 flex items-center gap-6 text-base">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span className="text-slate-600 font-medium">{wordCount} words</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span className="text-slate-600 font-medium">{charCount} characters</span>
                </div>
                {wordCount < 30 && (
                  <motion.div
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="flex items-center gap-2 px-4 py-2 bg-orange-50 border border-orange-200 rounded-full"
                  >
                    <TrendingUp className="w-4 h-4 text-orange-600" />
                    <span className="text-orange-700 font-semibold text-sm">
                      Add more detail for better feedback
                    </span>
                  </motion.div>
                )}
              </div>
            </div>

            <motion.button
              type="submit"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              disabled={loading}
              className="w-full px-8 py-5 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white rounded-2xl font-bold text-xl shadow-xl hover:shadow-2xl transition-all flex items-center justify-center gap-3 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <div className="w-6 h-6 border-3 border-white border-t-transparent rounded-full animate-spin" />
                  Processing Answer...
                </>
              ) : (
                <>
                  Submit Answer
                  <ArrowRight className="w-6 h-6" />
                </>
              )}
            </motion.button>
          </form>
        </motion.div>
      </div>
    </div>
  );
};

export default InterviewScreen;