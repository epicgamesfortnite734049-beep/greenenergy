import React from 'react';
import { ReceiptIcon } from './icons';

interface CarbonReceiptProps {
  text: string;
}

const CarbonReceipt: React.FC<CarbonReceiptProps> = ({ text }) => {
  return (
    <div className="mt-2 bg-yellow-50 dark:bg-gray-800/50 border-2 border-dashed border-gray-400 dark:border-gray-600 rounded-lg p-3 font-mono text-xs text-gray-800 dark:text-gray-300 shadow-inner">
        <div className="flex items-center justify-center gap-2 mb-2 border-b border-dashed border-gray-400 dark:border-gray-600 pb-2">
            <ReceiptIcon className="h-5 w-5" />
            <h3 className="font-bold text-center">Carbon Footprint Receipt</h3>
        </div>
        <pre className="whitespace-pre-wrap text-left">{text}</pre>
    </div>
  );
};

export default CarbonReceipt;
