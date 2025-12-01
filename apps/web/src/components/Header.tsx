import { ChevronLeft, Wifi, Battery, Signal } from "lucide-react";

interface HeaderProps {
  title?: string;
  showBackButton?: boolean;
  onBack?: () => void;
}

export function Header({ title, showBackButton = true, onBack }: HeaderProps) {
  return (
    <div className="bg-white px-4 py-3 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="text-sm">9:41</div>
      </div>

      <div className="flex items-center space-x-1">
        <Signal className="w-4 h-4" />
        <Wifi className="w-4 h-4" />
        <Battery className="w-4 h-4" />
      </div>
    </div>
  );
}
