import { motion } from 'framer-motion';
import { Trophy, Sparkles, AlertTriangle, MessageSquare, Download, RefreshCw, CheckCircle, XCircle } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, RadialBarChart, RadialBar, Legend } from 'recharts';

const DashboardScreen = ({ data, onRestart }) => {
  const { overall_score, strengths, critical_gaps, behavioral_feedback, hire_recommendation } = data;

  const scoreData = [
    { name: 'Score', value: overall_score, fill: '#8b5cf6' },
    { name: 'Remaining', value: 100 - overall_score, fill: '#e2e8f0' },
  ];

  const getScoreColor = (score) => {
    if (score >= 80) return 'from-green-500 to-emerald-500';
    if (score >= 60) return 'from-blue-500 to-cyan-500';
    if (score >= 40) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-pink-500';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
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
    <div className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full mb-6 shadow-lg">
            <Trophy className="w-10 h-10 text-white" />
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-3">
            Interview Complete! 🎉
          </h2>
          <p className="text-xl text-slate-600">
            Here's your comprehensive performance analysis
          </p>
        </motion.div>

        {/* Score Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-3xl shadow-2xl p-8 md:p-12 mb-8 border border-slate-200"
        >
          <div className="grid md:grid-cols-2 gap-8 items-center">
            {/* Score Circle */}
            <div className="flex flex-col items-center">
              <div className="relative w-64 h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <RadialBarChart
                    cx="50%"
                    cy="50%"
                    innerRadius="70%"
                    outerRadius="100%"
                    data={[{ value: overall_score, fill: '#8b5cf6' }]}
                    startAngle={90}
                    endAngle={-270}
                  >
                    <RadialBar
                      background
                      dataKey="value"
                      cornerRadius={10}
                    />
                  </RadialBarChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <div className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    {overall_score}
                  </div>
                  <div className="text-slate-600 font-medium">out of 100</div>
                </div>
              </div>
              <div className={`mt-6 px-6 py-3 bg-gradient-to-r ${getScoreColor(overall_score)} text-white rounded-full font-bold text-lg shadow-lg`}>
                {getScoreLabel(overall_score)}
              </div>
            </div>

            {/* Recommendation */}
            <div className="text-center md:text-left">
              <div className={`inline-flex items-center gap-3 px-6 py-4 rounded-2xl mb-6 ${
                hire_recommendation
                  ? 'bg-green-50 border-2 border-green-200'
                  : 'bg-orange-50 border-2 border-orange-200'
              }`}>
                {hire_recommendation ? (
                  <>
                    <CheckCircle className="w-8 h-8 text-green-600" />
                    <div>
                      <div className="font-bold text-green-900 text-xl">Hire Recommended</div>
                      <div className="text-green-700 text-sm">Strong candidate for the role</div>
                    </div>
                  </>
                ) : (
                  <>
                    <XCircle className="w-8 h-8 text-orange-600" />
                    <div>
                      <div className="font-bold text-orange-900 text-xl">More Practice Needed</div>
                      <div className="text-orange-700 text-sm">Review feedback and try again</div>
                    </div>
                  </>
                )}
              </div>
              <p className="text-slate-600 text-lg leading-relaxed">
                {hire_recommendation
                  ? "You demonstrated strong technical knowledge and communication skills. Keep up the excellent work!"
                  : "Focus on the improvement areas below and practice more to strengthen your interview performance."}
              </p>
            </div>
          </div>
        </motion.div>

        {/* Strengths */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-slate-200"
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-slate-900">Your Strengths</h3>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            {strengths.map((strength, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="flex items-start gap-3 p-4 bg-green-50 rounded-xl border border-green-200"
              >
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                <p className="text-slate-700">{strength}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Critical Gaps */}
        {critical_gaps && critical_gaps.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-slate-200"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
                <AlertTriangle className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-slate-900">Areas for Improvement</h3>
            </div>
            <div className="space-y-6">
              {critical_gaps.map((gap, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 + index * 0.1 }}
                  className="p-6 bg-orange-50 rounded-xl border border-orange-200"
                >
                  <div className="flex items-start gap-3 mb-3">
                    <div className="px-3 py-1 bg-orange-200 text-orange-900 rounded-full text-sm font-semibold">
                      {gap.panelist_flagged}
                    </div>
                    <h4 className="text-lg font-bold text-slate-900 flex-1">{gap.topic}</h4>
                  </div>
                  <div className="space-y-3 ml-3">
                    <div>
                      <div className="text-sm font-semibold text-slate-600 mb-1">What went wrong:</div>
                      <p className="text-slate-700">{gap.what_went_wrong}</p>
                    </div>
                    <div>
                      <div className="text-sm font-semibold text-slate-600 mb-1">How to fix:</div>
                      <p className="text-slate-700 font-medium">{gap.how_to_fix}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Behavioral Feedback */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-slate-200"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-xl flex items-center justify-center">
              <MessageSquare className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-slate-900">Behavioral Feedback</h3>
          </div>
          <p className="text-lg text-slate-700 leading-relaxed">{behavioral_feedback}</p>
        </motion.div>

        {/* Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
          className="flex flex-col sm:flex-row gap-4 justify-center"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={downloadReport}
            className="px-8 py-4 bg-white text-slate-700 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all border-2 border-slate-200 hover:border-slate-300 flex items-center justify-center gap-2"
          >
            <Download className="w-5 h-5" />
            Download Report
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onRestart}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2"
          >
            <RefreshCw className="w-5 h-5" />
            Start New Interview
          </motion.button>
        </motion.div>
      </div>
    </div>
  );
};

export default DashboardScreen;

// Made with Bob
