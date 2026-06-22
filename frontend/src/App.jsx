import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import WelcomeScreen from './components/WelcomeScreen';
import SetupScreen from './components/SetupScreen';
import InterviewScreen from './components/InterviewScreen';
import DashboardScreen from './components/DashboardScreen';

function App() {
  const [currentScreen, setCurrentScreen] = useState('welcome');
  const [sessionData, setSessionData] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);

  const screens = {
    welcome: <WelcomeScreen onNext={() => setCurrentScreen('setup')} />,
    setup: (
      <SetupScreen
        onBack={() => setCurrentScreen('welcome')}
        onStart={(data) => {
          setSessionData(data);
          setCurrentScreen('interview');
        }}
      />
    ),
    interview: (
      <InterviewScreen
        sessionData={sessionData}
        onComplete={(dashboard) => {
          setDashboardData(dashboard);
          setCurrentScreen('dashboard');
        }}
      />
    ),
    dashboard: (
      <DashboardScreen
        data={dashboardData}
        onRestart={() => {
          setSessionData(null);
          setDashboardData(null);
          setCurrentScreen('welcome');
        }}
      />
    ),
  };

  return (
    <div className="min-h-screen">
      <AnimatePresence mode="wait">
        <motion.div
          key={currentScreen}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          {screens[currentScreen]}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

export default App;

// Made with Bob
