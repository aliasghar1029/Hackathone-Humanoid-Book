import React from 'react';
import { useAuthModal } from '../contexts/AuthModalContext';
import AuthModal from './Auth/AuthModal';

const AuthModalWrapper = () => {
  const { isModalOpen, closeModal } = useAuthModal();

  return <AuthModal isOpen={isModalOpen} onClose={closeModal} />;
};

export default AuthModalWrapper;