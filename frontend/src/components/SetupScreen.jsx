import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, FileText, Briefcase, Sparkles } from 'lucide-react';
import { interviewAPI } from '../services/api';

const SetupScreen = ({ onBack, onStart }) => {
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLoadExample = async () => {
    try {
      setLoading(true);
      const data = await interviewAPI.loadExampleData();
      setResume(data.resume);
      setJobDescription(data.job_description);
      setError('');
    } catch (err) {
      setError('Failed to load example data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resume.trim() || !jobDescription.trim()) {
      setError('Please fill in both fields');
      return;
    }

    try {
      setLoading(true);
      setError('');
      const data = await interviewAPI.startInterview(resume, jobDescription);
      onStart(data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to start interview');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div className="max-w-5xl w-full">
        <motion.button
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          whileHover={{ x: -5 }}
          onClick={onBack}
          className="mb-8 flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors font-semibold"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Home
        </motion.button>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="bg-white rounded-3xl shadow-2xl p-10 md:p-16 border-2 border-slate-100"
        >
          <div className="text-center mb-12">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
              className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl mb-6 shadow-lg"
            >
              <Sparkles className="w-8 h-8 text-white" />
            </motion.div>
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
              Configure Your Interview
            </h2>
            <p className="text-xl text-slate-600">
              Provide your resume and target job description to begin
            </p>
          </div>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-8 p-5 bg-red-50 border-2 border-red-200 rounded-2xl text-red-700 font-medium"
            >
              {error}
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="space-y-8">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <label className="flex items-center gap-3 text-xl font-bold text-slate-900 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                Your Resume
              </label>
              <textarea
                value={resume}
                onChange={(e) => setResume(e.target.value)}
                placeholder="Paste your resume here... Include your experience, skills, and achievements."
                rows={10}
                className="w-full px-6 py-4 border-2 border-slate-200 rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all outline-none resize-none text-slate-700 text-lg"
                required
              />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <label className="flex items-center gap-3 text-xl font-bold text-slate-900 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                  <Briefcase className="w-5 h-5 text-white" />
                </div>
                Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here... Include requirements, responsibilities, and qualifications."
                rows={10}
                className="w-full px-6 py-4 border-2 border-slate-200 rounded-2xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all outline-none resize-none text-slate-700 text-lg"
                required
              />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex flex-col sm:flex-row gap-4 pt-4"
            >
              <motion.button
                type="button"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleLoadExample}
                disabled={loading}
                className="flex-1 px-8 py-5 bg-slate-100 text-slate-700 rounded-2xl font-bold text-lg hover:bg-slate-200 transition-colors flex items-center justify-center gap-3 disabled:opacity-50 border-2 border-slate-200"
              >
                <Sparkles className="w-6 h-6" />
                Load Example Data
              </motion.button>

              <motion.button
                type="submit"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                disabled={loading}
                className="flex-1 px-8 py-5 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white rounded-2xl font-bold text-lg shadow-xl hover:shadow-2xl transition-all flex items-center justify-center gap-3 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <div className="w-6 h-6 border-3 border-white border-t-transparent rounded-full animate-spin" />
                    Starting...
                  </>
                ) : (
                  <>
                    Begin Interview
                    <ArrowRight className="w-6 h-6" />
                  </>
                )}
              </motion.button>
            </motion.div>
          </form>
        </motion.div>
      </div>
    </div>
  );
};

export default SetupScreen;