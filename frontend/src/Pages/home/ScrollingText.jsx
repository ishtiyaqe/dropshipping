
import './asset/ScrollingText.css';

const ScrollingText = ({ text }) => {
  return (
    <div className="scrolling-text-container">
      <div className="scrolling-text">{text}</div>
    </div>
  );
};

export default ScrollingText;
