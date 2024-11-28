class Shellgpt < Formula
    desc "ShellGPT: Interact with OpenAI from the shell"
    homepage "https://github.com/adborroto/homebrew-shellgpt"
    url "https://github.com/adborroto/homebrew-shellgpt/archive/v1.2.0.tar.gz" 
    sha256 "714b48c1496b3858e38fe27bcea314dab3358882c29fbeee44e601d2ca233f4b"
    license "MIT"
  
    depends_on "python@3.10" 
  
    def install
        # Create a virtual environment in the libexec directory
        ENV.prepend_create_path "PYTHONPATH", libexec/"lib/python3.10/site-packages"
        system "python3", "-m", "venv", libexec
    
        # Install dependencies inside the virtual environment
        system libexec/"bin/pip", "install", "--upgrade", "pip", "setuptools", "wheel"
        system libexec/"bin/pip", "install", "openai"
    
        # Install the script
        libexec.install "shellgpt.py"
    
        # Create a wrapper script to call the script within the virtual environment
        (bin/"shellgpt").write <<~EOS
          #!/bin/bash
          #{libexec}/bin/python3 #{libexec}/shellgpt.py "$@"
        EOS
        chmod "+x", bin/"shellgpt"
    end
  
    test do
      system "#{bin}/shellgpt", "--help"
    end
  end
  