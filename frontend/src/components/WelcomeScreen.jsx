import { motion } from 'framer-motion';
import { Target, Users, Sparkles, ArrowRight, Play } from 'lucide-react';

const WelcomeScreen = ({ onNext }) => {
  const features = [
    {
      icon: <Users className="w-8 h-8" />,
      title: 'Hiring Manager',
      description: 'Behavioral & Leadership',
      color: 'from-blue-500 to-cyan-500',
      emoji: '🎭',
    },
    {
      icon: <Target className="w-8 h-8" />,
      title: 'System Architect',
      description: 'Design & Scalability',
      color: 'from-purple-500 to-pink-500',
      emoji: '🏗️',
    },
    {
      icon: <Sparkles className="w-8 h-8" />,
      title: 'Senior Developer',
      description: 'Technical Depth',
      color: 'from-orange-500 to-red-500',
      emoji: '💻',
    },
  ];

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div className="max-w-6xl w-full">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="text-center mb-20"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="inline-flex items-center gap-4 mb-8"
          >
            <div className="w-20 h-20 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-3xl flex items-center justify-center shadow-2xl transform hover:rotate-6 transition-transform">
              <span className="text-5xl">🎯</span>
            </div>
            <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              PanelPulse
            </h1>
          </motion.div>
          
          <motion.h2
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="text-5xl md:text-6xl font-bold text-slate-900 mb-8 leading-tight"
          >
            Master Your Interview with
            <br />
            <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              Multi-Agent Practice
            </span>
          </motion.h2>
          
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="text-2xl text-slate-600 max-w-3xl mx-auto leading-relaxed"
          >
            Experience a realistic technical interview with our specialized panel.
            Get instant feedback and actionable insights to ace your next interview.
          </motion.p>
        </motion.div>

        {/* Feature Cards */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.8 }}
          className="grid md:grid-cols-3 gap-8 mb-16"
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.0 + index * 0.15, duration: 0.6 }}
              whileHover={{ scale: 1.05, y: -8 }}
              className="bg-white rounded-3xl p-10 shadow-xl hover:shadow-2xl transition-all duration-300 border-2 border-slate-100 hover:border-slate-200"
            >
              <div className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center text-white mb-6 shadow-lg text-4xl`}>
                {feature.emoji}
              </div>
              <h3 className="text-2xl font-bold text-slate-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-lg text-slate-600">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.5, duration: 0.8 }}
          className="flex flex-col sm:flex-row gap-6 justify-center items-center"
        >
          <motion.button
            whileHover={{ scale: 1.08 }}
            whileTap={{ scale: 0.95 }}
            onClick={onNext}
            className="group px-12 py-5 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white rounded-2xl font-bold text-xl shadow-2xl hover:shadow-3xl transition-all duration-300 flex items-center gap-3"
          >
            Start Interview
            <ArrowRight className="w-6 h-6 group-hover:translate-x-2 transition-transform" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.08 }}
            whileTap={{ scale: 0.95 }}
            className="px-12 py-5 bg-white text-slate-700 rounded-2xl font-bold text-xl shadow-xl hover:shadow-2xl transition-all duration-300 border-2 border-slate-200 hover:border-slate-300 flex items-center gap-3"
          >
            <Play className="w-6 h-6" />
            View Demo
          </motion.button>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.8, duration: 0.8 }}
          className="mt-20 grid grid-cols-3 gap-12 max-w-4xl mx-auto"
        >
          {[
            { value: '6', label: 'Questions', color: 'from-blue-600 to-cyan-600' },
            { value: '3', label: 'Panelists', color: 'from-purple-600 to-pink-600' },
            { value: '100%', label: 'Feedback', color: 'from-orange-600 to-red-600' },
          ].map((stat, index) => (
            <motion.div
              key={index}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 2.0 + index * 0.1, type: "spring" }}
              className="text-center"
            >
              <div className={`text-5xl font-bold bg-gradient-to-r ${stat.color} bg-clip-text text-transparent mb-3`}>
                {stat.value}
              </div>
              <div className="text-slate-600 font-semibold text-lg">{stat.label}</div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </div>
  );
};

export default WelcomeScreen;