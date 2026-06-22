import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, MessageSquare, User } from 'lucide-react';
import { interviewAPI } from '../services/api';

const panelistInfo = {
  'hiring-manager': {
    name: 'Hiring Manager',
    role: 'Behavioral & Leadership',
    icon: '👔',
    color: 'from-blue-500 to-cyan-500',
  },
  'system-architect': {
    name: 'System Architect',
    role: 'Design & Scalability',
    icon: '🏗️',
    color: 'from-purple-500 to-pink-500',
  },
  'senior-dev': {
    name: 'Senior Developer',
    role: 'Technical Depth & Debugging',
    icon: '💻',
    color: 'from-orange-500 to-red-500',
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
    <div className="min-h-screen p-6">
      <div className="max-w-5xl mx-auto">
        {/* Progress Bar */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex justify-between items-center mb-3">
            <span className="text-sm font-semibold text-slate-600">
              Interview Progress
            </span>
            <span className="text-sm font-bold text-slate-900">
              {questionNumber} / {totalQuestions}
            </span>
          </div>
          <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5 }}
              className="h-full bg-gradient-to-r from-blue-600 to-purple-600 rounded-full"
            />
          </div>
        </motion.div>

        {/* Panelist Card */}
        <motion.div
          key={currentPanelist}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white rounded-2xl shadow-lg p-6 mb-6 border border-slate-200"
        >
          <div className="flex items-center gap-4">
            <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${panelist.color} flex items-center justify-center text-3xl shadow-lg`}>
              {panelist.icon}
            </div>
            <div>
              <h3 className="text-xl font-bold text-slate-900">{panelist.name}</h3>
              <p className="text-slate-600">{panelist.role}</p>
            </div>
          </div>
        </motion.div>

        {/* Question Card */}
        <motion.div
          key={currentQuestion}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-white to-slate-50 rounded-2xl shadow-xl p-8 mb-6 border border-slate-200"
        >
          <div className="flex items-start gap-3 mb-4">
            <MessageSquare className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
            <div>
              <h4 className="text-sm font-semibold text-slate-500 mb-2">QUESTION</h4>
              <p className="text-lg text-slate-900 leading-relaxed whitespace-pre-wrap">
                {currentQuestion}
              </p>
            </div>
          </div>
        </motion.div>

        {/* Answer Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-2xl shadow-xl p-8 border border-slate-200"
        >
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700"
            >
              {error}
            </motion.div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="flex items-center gap-2 text-lg font-semibold text-slate-900 mb-3">
                <User className="w-5 h-5 text-purple-600" />
                Your Answer
              </label>
              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Type your answer here... Be specific and provide concrete examples."
                rows={8}
                className="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all outline-none resize-none text-slate-700"
                required
                disabled={loading}
              />
              <div className="mt-3 flex items-center gap-4 text-sm text-slate-500">
                <span>{wordCount} words</span>
                <span>•</span>
                <span>{charCount} characters</span>
                {wordCount < 20 && (
                  <>
                    <span>•</span>
                    <span className="text-orange-600 font-medium">
                      Tip: Provide more detail for better feedback
                    </span>
                  </>
                )}
              </div>
            </div>

            <motion.button
              type="submit"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              disabled={loading}
              className="w-full px-6 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  Submit Answer
                  <ArrowRight className="w-5 h-5" />
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

// Made with Bob
