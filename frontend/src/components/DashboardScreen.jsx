import { motion } from 'framer-motion';
import { Trophy, Sparkles, AlertTriangle, MessageSquare, Download, RefreshCw, CheckCircle, XCircle, Award, TrendingUp } from 'lucide-react';
import { RadialBarChart, RadialBar, ResponsiveContainer } from 'recharts';

const DashboardScreen = ({ data, onRestart }) => {
  const { overall_score, strengths, critical_gaps, behavioral_feedback, hire_recommendation } = data;

  const getScoreColor = (score) => {
    if (score >= 80) return 'from-green-500 to-emerald-500';
    if (score >= 60) return 'from-blue-500 to-cyan-500';
    if (score >= 40) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-pink-500';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent Performance';
    if (score >= 60) return 'Good Performance';
    if (score >= 40) return 'Fair Performance';
    return 'Needs Improvement';
  };

  const downloadReport = () => {
    const reportData = JSON.stringify(data, null, 2);
    const blob = new Blob([reportData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `panelpulse-report-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-3xl mb-8 shadow-2xl"
          >
            <Trophy className="w-12 h-12 text-white" />
          </motion.div>
          <h2 className="text-5xl md:text-6xl font-bold text-slate-900 mb-4">
            Interview Complete! 🎉
          </h2>
          <p className="text-2xl text-slate-600">
            Here's your comprehensive performance analysis
          </p>
        </motion.div>

        {/* Score Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="bg-white rounded-3xl shadow-2xl p-12 md:p-16 mb-12 border-2 border-slate-100"
        >
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Score Circle */}
            <div className="flex flex-col items-center">
              <div className="relative w-72 h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <RadialBarChart
                    cx="50%"
                    cy="50%"
                    innerRadius="75%"
                    outerRadius="100%"
                    data={[{ value: overall_score, fill: 'url(#scoreGradient)' }]}
                    startAngle={90}
                    endAngle={-270}
                  >
                    <defs>
                      <linearGradient id="scoreGradient" x1="0" y1="0" x2="1" y2="1">
                        <stop offset="0%" stopColor="#3b82f6" />
                        <stop offset="50%" stopColor="#8b5cf6" />
                        <stop offset="100%" stopColor="#ec4899" />
                      </linearGradient>
                    </defs>
                    <RadialBar
                      background={{ fill: '#e2e8f0' }}
                      dataKey="value"
                      cornerRadius={20}
                    />
                  </RadialBarChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <div className="text-7xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                    {overall_score}
                  </div>
                  <div className="text-slate-600 font-semibold text-xl mt-2">out of 100</div>
                </div>
              </div>
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.6, type: "spring" }}
                className={`mt-8 px-8 py-4 bg-gradient-to-r ${getScoreColor(overall_score)} text-white rounded-2xl font-bold text-xl shadow-xl`}
              >
                {getScoreLabel(overall_score)}
              </motion.div>
            </div>

            {/* Recommendation */}
            <div className="text-center md:text-left">
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 }}
                className={`inline-flex items-center gap-4 px-8 py-6 rounded-3xl mb-8 ${
                  hire_recommendation
                    ? 'bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200'
                    : 'bg-gradient-to-br from-orange-50 to-red-50 border-2 border-orange-200'
                }`}
              >
                {hire_recommendation ? (
                  <>
                    <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center shadow-lg">
                      <CheckCircle className="w-8 h-8 text-white" />
                    </div>
                    <div>
                      <div className="font-bold text-green-900 text-2xl mb-1">Hire Recommended</div>
                      <div className="text-green-700 text-lg">Strong candidate for the role</div>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center shadow-lg">
                      <XCircle className="w-8 h-8 text-white" />
                    </div>
                    <div>
                      <div className="font-bold text-orange-900 text-2xl mb-1">More Practice Needed</div>
                      <div className="text-orange-700 text-lg">Review feedback and try again</div>
                    </div>
                  </>
                )}
              </motion.div>
              <p className="text-slate-700 text-xl leading-relaxed">
                {hire_recommendation
                  ? "You demonstrated strong technical knowledge and excellent communication skills. Keep up the outstanding work!"
                  : "Focus on the improvement areas below and practice more to strengthen your interview performance. You're on the right track!"}
              </p>
            </div>
          </div>
        </motion.div>

        {/* Feedback Grid */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {/* Strengths */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="bg-white rounded-3xl shadow-xl p-10 border-2 border-slate-100"
          >
            <div className="flex items-center gap-4 mb-8">
              <div className="w-14 h-14 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center shadow-lg">
                <Sparkles className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-slate-900">Your Strengths</h3>
            </div>
            <div className="space-y-4">
              {strengths.map((strength, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 + index * 0.1 }}
                  className="flex items-start gap-4 p-5 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl border-2 border-green-200"
                >
                  <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-0.5" />
                  <p className="text-slate-700 text-lg leading-relaxed">{strength}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Critical Gaps */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="bg-white rounded-3xl shadow-xl p-10 border-2 border-slate-100"
          >
            <div className="flex items-center gap-4 mb-8">
              <div className="w-14 h-14 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center shadow-lg">
                <AlertTriangle className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-slate-900">Areas to Improve</h3>
            </div>
            {critical_gaps && critical_gaps.length > 0 ? (
              <div className="space-y-6">
                {critical_gaps.map((gap, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.7 + index * 0.1 }}
                    className="p-6 bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl border-2 border-orange-200"
                  >
                    <div className="flex items-start gap-3 mb-4">
                      <div className="px-4 py-2 bg-orange-200 text-orange-900 rounded-xl text-sm font-bold uppercase tracking-wide">
                        {gap.panelist_flagged}
                      </div>
                      <h4 className="text-xl font-bold text-slate-900 flex-1">{gap.topic}</h4>
                    </div>
                    <div className="space-y-4 ml-2">
                      <div>
                        <div className="text-sm font-bold text-slate-600 mb-2 uppercase tracking-wide">Issue:</div>
                        <p className="text-slate-700 text-lg leading-relaxed">{gap.what_went_wrong}</p>
                      </div>
                      <div>
                        <div className="text-sm font-bold text-slate-600 mb-2 uppercase tracking-wide">Solution:</div>
                        <p className="text-slate-900 font-semibold text-lg leading-relaxed">{gap.how_to_fix}</p>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Award className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <p className="text-slate-600 text-lg">No critical gaps identified! Excellent work!</p>
              </div>
            )}
          </motion.div>
        </div>

        {/* Behavioral Feedback */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
          className="bg-white rounded-3xl shadow-xl p-10 mb-12 border-2 border-slate-100"
        >
          <div className="flex items-center gap-4 mb-6">
            <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl flex items-center justify-center shadow-lg">
              <MessageSquare className="w-7 h-7 text-white" />
            </div>
            <h3 className="text-3xl font-bold text-slate-900">Behavioral Feedback</h3>
          </div>
          <p className="text-xl text-slate-700 leading-relaxed">{behavioral_feedback}</p>
        </motion.div>

        {/* Actions */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.1 }}
          className="flex flex-col sm:flex-row gap-6 justify-center"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={downloadReport}
            className="px-10 py-5 bg-white text-slate-700 rounded-2xl font-bold text-xl shadow-xl hover:shadow-2xl transition-all border-2 border-slate-200 hover:border-slate-300 flex items-center justify-center gap-3"
          >
            <Download className="w-6 h-6" />
            Download Report
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onRestart}
            className="px-10 py-5 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white rounded-2xl font-bold text-xl shadow-xl hover:shadow-2xl transition-all flex items-center justify-center gap-3"
          >
            <RefreshCw className="w-6 h-6" />
            Start New Interview
          </motion.button>
        </motion.div>
      </div>
    </div>
  );
};

export default DashboardScreen;