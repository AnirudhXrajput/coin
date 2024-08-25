import React, { useState } from 'react';
import Web3 from 'web3';
import CoinFlipABI from './CoinFlipABI.json';

const CoinFlip = () => {
    const [account, setAccount] = useState('');
    const [amount, setAmount] = useState('');
    const [guess, setGuess] = useState(true);
    const [message, setMessage] = useState('');

    const web3 = new Web3(Web3.givenProvider);
    const contractAddress = 'YOUR_CONTRACT_ADDRESS';
    const contract = new web3.eth.Contract(CoinFlipABI, contractAddress);

    const connectWallet = async () => {
        const accounts = await web3.eth.requestAccounts();
        setAccount(accounts[0]);
    };

    const flipCoin = async () => {
        try {
            await contract.methods.flip(guess).send({
                from: account,
                value: web3.utils.toWei(amount, 'ether')
            });
            setMessage('Transaction successful!');
        } catch (error) {
            setMessage('Transaction failed!');
        }
    };

    return (
        <div>
            <button onClick={connectWallet}>Connect Wallet</button>
            <div>
                <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="Amount in ETH"
                />
                <select onChange={(e) => setGuess(e.target.value === 'true')}>
                    <option value="true">Heads</option>
                    <option value="false">Tails</option>
                </select>
                <button onClick={flipCoin}>Flip Coin</button>
            </div>
            <p>{message}</p>
        </div>
    );
};

export default CoinFlip;
