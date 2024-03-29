import React, { useState } from "react";
import { JsonRpcProvider } from "@ethersproject/providers";
import { ethers } from "ethers";
import { InputBox__factory } from "@cartesi/rollups";
import { Input, Button, useToast } from "@chakra-ui/react";

// OBS: change Echo DApp address as appropriate
const DAPP_ADDRESS = "0x70ac08179605AF2D9e75782b8DEcDD3c22aA4D0C";

// Standard configuration for local development environment
const INPUTBOX_ADDRESS = "0x59b22D57D4f067708AB0c00552767405926dc768";
const HARDHAT_DEFAULT_MNEMONIC =
    "test test test test test test test test test test test junk";
const HARDHAT_LOCALHOST_RPC_URL = "http://localhost:8545";

interface ButtonProps {
    // Define the interface for buttonProps here
    isLoading: boolean;
    // Other properties if applicable
}

interface OwareInputProps {
    accountIndex: number;
    // Other props if applicable
}

// This component presents an input field and adds its contents as an input for the Echo DApp
function OwareInput() {
    const [value, setValue] = useState("");
    const [accountIndex] = useState(0);
    const toast = useToast();
    const [loading, setLoading] = useState(false);

    function handleSubmit(event: { preventDefault: () => void; }) {
        event.preventDefault();
        const sendInput = async () => {
            setLoading(true);
            // Start a connection
            const provider = new JsonRpcProvider(HARDHAT_LOCALHOST_RPC_URL);
            const signer = ethers.Wallet.fromMnemonic(
                HARDHAT_DEFAULT_MNEMONIC,
                `m/44'/60'/0'/0/${accountIndex}`
            ).connect(provider);

            // Instantiate the InputBox contract
            const inputBox = InputBox__factory.connect(
                INPUTBOX_ADDRESS,
                signer
            );


            const hardcodedPayload = '{"method":"agent_move","args":{"name":"agent","board_state":{"House1":{"seeds":["seed1","seed2","seed3","seed4"],"seeds_number":4},"House2":{"seeds":["seed5","seed6","seed7","seed8"],"seeds_number":4},"House3":{"seeds":["seed9","seed10","seed11","seed12"],"seeds_number":4},"House4":{"seeds":["seed13","seed14","seed15","seed16"],"seeds_number":4},"House5":{"seeds":["seed17","seed18","seed19","seed20"],"seeds_number":4},"House6":{"seeds":["seed21","seed22","seed23","seed24"],"seeds_number":4},"House7":{"seeds":["seed25","seed26","seed27","seed28"],"seeds_number":4},"House8":{"seeds":["seed29","seed30","seed31","seed32"],"seeds_number":4},"House9":{"seeds":["seed33","seed34","seed35","seed36"],"seeds_number":4},"House10":{"seeds":["seed37","seed38","seed39","seed40"],"seeds_number":4},"House11":{"seeds":["seed41","seed42","seed43","seed44"],"seeds_number":4},"House12":{"seeds":["seed45","seed46","seed47","seed48"],"seeds_number":4}}}}';

            // Encode the input
            const inputBytes = ethers.utils.toUtf8Bytes(hardcodedPayload);


            // Send the transaction
            const tx = await inputBox.addInput(DAPP_ADDRESS, inputBytes);
            console.log(`transaction: ${tx.hash}`);
            toast({
                title: "Transaction Sent",
                description: "waiting for confirmation",
                status: "success",
                duration: 9000,
                isClosable: true,
                position: "top-left",
            });

            // Wait for confirmation
            console.log("waiting for confirmation...");
            const receipt = await tx.wait(1);

            // Search for the InputAdded event
            const event = receipt.events?.find((e) => e.event === "InputAdded");

            setLoading(false);
            toast({
                title: "Transaction Confirmed",
                description: `Input added => index: ${event?.args?.inputIndex} `,
                status: "success",
                duration: 9000,
                isClosable: true,
                position: "top-left",
            });
            console.log(`Input added => index: ${event?.args?.inputIndex} `);
        };
        sendInput();
    }

    function handleChange(event: { target: { value: React.SetStateAction<string>; }; }) {
        setValue(event.target.value);
    }

    let buttonProps:ButtonProps = {
        isLoading: false
    };

    if (loading) {
        buttonProps.isLoading = true;
    }
    
    return (
        <div>
            <img className="monster" src="/monster.jpg" alt="monster" />
            <a
                className="link"
                href="https://www.freepik.com/free-vector/monster-cartoon-yellow-background-with-image-creepy-one-eyed-horned-creature-with-terrible-grin-vector-illustration_31643399.htm#query=monster%20cartoon&position=2&from_view=keyword#position=2&query=monster%20cartoon"
            >
                Image by macrovector on Freepik{" "}
            </a>
            <form onSubmit={handleSubmit}>
                <label>
                    <p>Roar something!</p>
                </label>
                <Input
                    type="text"
                    focusBorderColor="yellow"
                    size="md"
                    value={value}
                    onChange={handleChange}
                ></Input>
                <Button {...buttonProps} type="submit" colorScheme="yellow">
                    Roar
                </Button>
            </form>
        </div>
    );
}

export default OwareInput;
