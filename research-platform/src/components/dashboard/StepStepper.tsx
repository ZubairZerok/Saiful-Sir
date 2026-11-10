'use client';

import React from 'react';
import Link from 'next/link';
import { Check } from 'lucide-react';
import type { WorkflowStep } from '@/types';

interface StepStepperProps {
  steps: WorkflowStep[];
}

export function StepStepper({ steps }: StepStepperProps) {
  return (
    <div className="pipeline">
      <div className="pipeline__title">
        17-Step Auditinsyt Research Pipeline
      </div>

      <div className="pipeline__track">
        {steps.map((step, idx) => {
          let nodeCls = 'pipeline__step-node';
          let connCls = 'pipeline__step-connector';

          if (step.status === 'approved') {
            nodeCls += ' pipeline__step-node--approved';
            connCls += ' pipeline__step-connector--approved';
          } else if (step.status === 'in_progress') {
            nodeCls += ' pipeline__step-node--progress';
          } else if (step.status === 'review_requested') {
            nodeCls += ' pipeline__step-node--review';
          } else if (step.status === 'changes_requested') {
            nodeCls += ' pipeline__step-node--changes';
          } else if (step.status === 'locked') {
            nodeCls += ' pipeline__step-node--locked';
          }

          return (
            <Link
              key={step.number}
              href={`/steps/${step.number}`}
              className="pipeline__step"
              title={`Step ${step.number}: ${step.name}\nStatus: ${step.status}\n${step.description}`}
            >
              {idx < steps.length - 1 && <div className={connCls} />}
              <div className={nodeCls}>
                {step.status === 'approved' ? (
                  <Check size={12} strokeWidth={3} aria-hidden="true" />
                ) : (
                  step.number
                )}
              </div>
              <span className="pipeline__step-label">{step.name}</span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
