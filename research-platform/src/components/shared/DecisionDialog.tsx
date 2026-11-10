'use client';

import React, { useState } from 'react';

interface DecisionDialogProps {
  stepNumber: number;
  stepName: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export function DecisionDialog({
  stepNumber,
  stepName,
  isOpen,
  onClose,
  onSuccess,
}: DecisionDialogProps) {
  const [decision, setDecision] = useState<'approved' | 'changes_requested' | 'locked'>('approved');
  const [rationale, setRationale] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!rationale.trim()) return;

    setIsSubmitting(true);
    try {
      // Save decision to localStorage
      const dec = {
        id: `dec-${Date.now()}`,
        stepId: `step-${stepNumber}`,
        decision,
        rationale,
        decidedBy: 'Supervisor / Lead Auditor',
        decidedAt: new Date().toISOString(),
      };
      try {
        const existing = JSON.parse(localStorage.getItem('auditinsyt_decisions') || '[]');
        localStorage.setItem('auditinsyt_decisions', JSON.stringify([dec, ...existing]));
      } catch {}

      onSuccess();
      onClose();
    } catch (e) {
      console.error('Failed to submit step review decision', e);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="decision-dialog__overlay" onClick={onClose}>
      <div className="decision-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="decision-dialog__title">
          STEP {stepNumber} SUPERVISOR AUDIT REVIEW
        </div>
        <div style={{ fontSize: '13px', color: 'var(--color-text-secondary)', marginBottom: '16px' }}>
          {stepName}
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: 700, color: 'var(--color-text-muted)', marginBottom: '6px' }}>
              AUDIT DECISION
            </label>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                type="button"
                onClick={() => setDecision('approved')}
                className={`btn ${decision === 'approved' ? 'btn--primary' : 'btn--secondary'}`}
                style={{ flex: 1, fontSize: '11px' }}
              >
                Approve Step
              </button>
              <button
                type="button"
                onClick={() => setDecision('changes_requested')}
                className={`btn ${decision === 'changes_requested' ? 'btn--danger' : 'btn--secondary'}`}
                style={{ flex: 1, fontSize: '11px' }}
              >
                Request Changes
              </button>
            </div>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: 700, color: 'var(--color-text-muted)', marginBottom: '6px' }}>
              FORMAL AUDIT RATIONALE (REQUIRED)
            </label>
            <textarea
              className="decision-dialog__textarea"
              placeholder="Provide econometric, data quality, or methodology justification..."
              value={rationale}
              onChange={(e) => setRationale(e.target.value)}
              rows={4}
              required
            />
          </div>

          <div className="decision-dialog__actions">
            <button
              type="button"
              onClick={onClose}
              className="btn btn--secondary"
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn--primary"
              disabled={isSubmitting || !rationale.trim()}
            >
              {isSubmitting ? 'Recording...' : 'Submit Decision'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
