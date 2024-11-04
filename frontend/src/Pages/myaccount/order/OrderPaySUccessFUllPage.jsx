import Confetti from 'react-confetti';

const OrderPaySUccesssFUllPage = ({ data }) => {

const onClosesclass = () => {
    window.location.reload();
}

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm ">



            <div className="order-details-popup border rounded-md  shadow-md dark:shadow-gray-200 bg-white w-64 p-4 text-black">
                <div className="popup-content">
                    <div>🎉🎉 {data}</div>
                    <h2 className="flex justify-center">
                        <button
                            className="rounded-md shadow-md dark:shadow-gray-200 bg-red-600 text-white p-1"
                            onClick={onClosesclass}
                        >
                            Close
                        </button>
                    </h2>
                    <Confetti width={window.innerWidth} height={window.innerHeight} />
                </div>
            </div>
        </div>
    );
};

export default OrderPaySUccesssFUllPage;
