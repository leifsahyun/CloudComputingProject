In order to run the code properly, you need to setup keys to access each provider and to ssh into instances created by the providers.
template_keys.json contains a template of the information that the code requires in order to access the providers and acquire instances throught them. Use the template_keys.json file to create a keys.json file with all the values filled in.

Additionally, in order to ssh into instances acquired by the system (and for the system to ssh into instances), you must register an ssh keypair with each provider and place the private key in this folder as a \*.pem file. There should already be static_pair.pem and static_pair.public files in this folder, which you can register with the providers.

Finally, Google Compute Engine requires its own json keyfile to function. When you create a project service account, you will be able to download the keyfile. It may be handy to place it in this folder, but it is not necessary as long as the path to the file is defined in keys.json

Another note about setting up provider interfaces: In order to use the ArbitraryDriver with Amazon EC2, you must either allow inbound ssh traffic in your default Security Group in the AWS web interface, or create a new Security Group that allows such traffic and supply it to ArbitraryDriver.create_node(ex_security_groups). This does not involve the key files.