// Iceblox
// By Karl Hornell, April 8 1996

import java.awt.*;
import java.awt.image.*;
import java.io.UnsupportedEncodingException;
import java.net.*;
import java.util.Random;

public final class iceblox extends java.applet.Applet implements Runnable
{
	int i,j,k;
	final int playX=390,playY=330,mainX=390,mainY=348,smalls=48,blockX=13,blockY=11;
	final int animP[]={7,8,9,8,10,11,12,11,4,5,6,5,1,2,3,2};
	final int animF[]={32,33,34,35,36,35,34,33};
	final int levFlame[]={2,3,4,2,3,4},levRock[]={5,6,7,8,9,10};
	final int levSpeed[]={3,3,3,5,5,5},levIce[]={35,33,31,29,27,25};
	final int effMax=5;
	int playArea[];
	int gameState,counter,dir,inFront,inFront2,level,coins;
	int effLevel,lives=3;
	int x[],y[],dx[],dy[],motion[],look[],creature[],ccount[],actors,flames;
	int sideIX[]={0,-1,1,-15,15},coorDx[]={0,-30,30,0,0},coorDy[]={0,0,0,-30,30};
	Image collection,offImage,playField,small[],title;
	Graphics offGraphics,playGraphics,tempG;
	MediaTracker tracker;
	ImageFilter filter;
	ImageProducer collectionProducer;
	long snooze=100,score;
	Thread game;
	Math m;
	Random mm;
	byte[] b=null;

	public void init()
	{
		setBackground(Color.black);
		offImage=createImage(mainX,mainY);
		offGraphics=offImage.getGraphics();
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(0,0,mainX,mainY);
		playField=createImage(playX,playY);
		playGraphics=playField.getGraphics();
		playGraphics.setColor(Color.black);
		tracker=new MediaTracker(this);
		collection = getImage(getCodeBase(),"iceblox.gif");
		tracker.addImage(collection,0);
		try
		{
			tracker.waitForID(0);
		}
			catch(InterruptedException e) {}
		collectionProducer=collection.getSource();
		small=new Image[smalls];
		k=0;i=0;j=0;
		while (k<smalls)
		{
			filter=new CropImageFilter(j*30,i*30,30,30);
			small[k]=createImage(new FilteredImageSource(
				collectionProducer,filter));
			tracker.addImage(small[k],1);

			k++;
			j++;
			if (j==8)
			{
				j=0;
				i++;
			}
		}
		filter=new CropImageFilter(0,180,224,64);
		title=createImage(new FilteredImageSource(
				collectionProducer,filter));
		tracker.addImage(title,1);
		
		playArea=new int[(blockX+2)*(blockY+3)];
		x=new int[20];
		y=new int[20];
		dx=new int[20];
		dy=new int[20];
		look=new int[20];
		motion=new int[20];
		creature=new int[20];
		ccount=new int[20];
		
		gameState=7;
		try
		{
			tracker.waitForID(1);
		}
			catch(InterruptedException e) {}

		resize(mainX,mainY);
	}

	public void run()
	{
		while (game !=null)
		{
			try
			{
				game.sleep(snooze);
			} catch (InterruptedException e) {}
			counter=(counter+1)&255;
			switch (gameState)
			{
				case 0:
					prepareField();
					break;
				case 1:
					showField();
					break;
				case 2:
					gameLoop();
					break;
				case 3:
					happyPenguin();
					break;
				case 4:
					clearField();
					break;
				case 5:
					fixDeath();
					break;
				case 6:
					gameOver();
					break;
				case 7:
					drawIntro1();
					break;
				case 8:
					waitIntro1();
					break;
				case 9:
					drawIntro2();
					break;
				case 10:
					waitIntro2();
					break;
				case 11:
					drawIntro3();
					break;
				case 12:
					waitIntro3();
					break;
				case 13:
					drawFlag();
					break;
				default:
					break;
			}
			repaint();
		}
	}

	public void start()
	{
		if (game==null)
		{
			game=new Thread(this);
			game.start();
		}
	}

	public void stop()
	{
		if ((game!=null)&&(game.isAlive()))
		{
			game.stop();
		}
		game=null;
	}

	public boolean keyDown(java.awt.Event e,int key)
	{
		if (gameState==2)
		{
			switch (key)
			{
				case 97:
					dir=1; // A:Left
					break;
				case 100:
					dir=2; // D:Right
					break;
				case 107:
					dir=3; // K:Up
					break;
				case 109:
					dir=4; // M:Down
					break;
				default:
					break;
			}
		}
		else if ((gameState>6)&&(key==32))
			gameState=0;
		return false;
	}
	
	public boolean keyUp(java.awt.Event e,int key)
	{
		dir=0;
		return false;
	}

  // To ensure Java 1.1 compatibility, request focus on mouseDown
	public boolean mouseDown(java.awt.Event e,int x, int y)
	{
		requestFocus();
		return false;
	}
	
	public void prepareField()
	{
		int i;
		if (level>effMax)
			effLevel=effMax;
		else
			effLevel=level;
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(0,0,mainX,mainY);
		playGraphics.setColor(Color.black);
		playGraphics.fillRect(0,0,playX,playY);
		offGraphics.setColor(Color.lightGray);
		offGraphics.fill3DRect(0,mainY-playY-4,mainX,4,true);
		offGraphics.setColor(Color.white);
		offGraphics.drawString("SCORE:",2,12);
		updateScore(0);
		offGraphics.drawString("LEVEL:  "+(level+1),125,12);
		offGraphics.drawString("SPARE LIVES:",220,12);
		for (i=0;i<lives;i++)
			offGraphics.drawImage(small[13],300+i*15,-16,this);

		buildMap();

		gameState=1;
		snooze=100;
		counter=0;
		motion[0]=0;
		actors=1;
		coins=0;
		flames=0;
		look[0]=0;
		x[0]=30;
		y[0]=30;
		dx[0]=6;
		dy[0]=6;
		look[0]=2;
		creature[0]=1;
		for (i=0;i<20;i++)
			ccount[i]=0;
	}

	public void buildMap()
	{
		boolean notDone=true;
		int i,j,p,q;
		int stack[]=new int[blockX*blockY];
		
		for (i=0;i<(blockX+2)*(blockY+3);i++)
			playArea[i]=255;
		while (notDone)
		{
			for (i=1;i<=blockY;i++)
				for (j=1;j<=blockX;j++)
					playArea[i*(blockX+2)+j]=0;
			playArea[blockX+3]=-1; // Make room for start square

			i=0;
			j=5+levIce[effLevel]+levRock[effLevel];
			while (i<j) // Coins
			{
				p=1+(int)(mm.nextDouble()*blockX);
				q=1+(int)(mm.nextDouble()*blockY);
				if (playArea[q*(blockX+2)+p]==0)
				{
					if (i<5)
						playArea[q*(blockX+2)+p]=10; // Frozen coin
					else if (i<levIce[effLevel]+5)
						playArea[q*(blockX+2)+p]=2; // Ice cube
					else
						playArea[q*(blockX+2)+p]=1; // Rock
					i++;
				}
			}
			playArea[blockX+3]=0; // Clear start square
			p=0;
			q=1;
			i=0;
			stack[0]=blockX+3;
			while (p<q)
			{
				j=stack[p++];
				if ((playArea[j-blockX-2]&17)==0)
				{
					stack[q]=j-blockX-2;
					if (playArea[stack[q]]==10)
						i++;
					playArea[stack[q++]]|=16;
				}
				if ((playArea[j+blockX+2]&17)==0)
				{
					stack[q]=j+blockX+2;
					if (playArea[stack[q]]==10)
						i++;
					playArea[stack[q++]]|=16;
				}
				if ((playArea[j-1]&17)==0)
				{
					stack[q]=j-1;
					if (playArea[stack[q]]==10)
						i++;
					playArea[stack[q++]]|=16;
				}
				if ((playArea[j+1]&17)==0)
				{
					stack[q]=j+1;
					if (playArea[stack[q]]==10)
						i++;
					playArea[stack[q++]]|=16;
				}
			}
			notDone=i<5;
		}
		
		for (i=0;i<blockY;i++)
			for (j=0;j<blockX;j++)
			{
				p=(i+1)*(blockX+2)+j+1;
				playArea[p]&=15;
				switch(playArea[p])
				{
					case 1:
						playGraphics.drawImage(small[14],j*30,i*30,this);
						break;
					case 2:
						playGraphics.drawImage(small[16],j*30,i*30,this);
						break;
					case 10:
						playGraphics.drawImage(small[24],j*30,i*30,this);
						break;
					default:
						break;
				}
			}
	}

	public void showField()
	{
		Graphics saveGraphics;
		saveGraphics=offGraphics.create();
		offGraphics.clipRect(playX/2-(counter*playX/2/30),mainY-playY+
		playY/2-(counter*playY/2/30),counter*playX/30,counter*playY/30);
		offGraphics.drawImage(playField,0,mainY-playY,this);
		if (counter==30)
		{
			gameState=2;
			snooze=100;
		}
		offGraphics=saveGraphics;
	}

	public void gameLoop()
	{
		if (flames<levFlame[effLevel])
		{
			if (x[0]<(playX/2))
				x[actors]=playX+30;
			else
				x[actors]=0;
			y[actors]=30*(1+(int)(m.random()*blockY));
			j=(y[actors]/30)*(blockX+2)+x[actors]/30;
			motion[actors]=0;
			dx[actors]=levSpeed[effLevel];
			dy[actors]=levSpeed[effLevel];
			creature[actors]=4;
			if ((playArea[j+1]==0)||(playArea[j-1]==0))
			{
				actors++;
				flames++;
			}
		}
		for (i=0;i<actors;i++)
		{
			ccount[i]++;
			switch(motion[i])
			{
				case 1:
					x[i]-=dx[i];
					break;
				case 2:
					x[i]+=dx[i];
					break;
				case 3:
					y[i]-=dy[i];
					break;
				case 4:
					y[i]+=dy[i];
					break;
				default:
					break;
			}
			j=(y[i]/30)*(blockX+2)+x[i]/30;
			switch(creature[i])
			{
				case 1: // Penguin
					if ((x[i]%30 == 0)&&(y[i]%30 == 0))
						motion[i]=0;
					if (motion[i]==0)
					{
						inFront=playArea[j+sideIX[dir]];
						if ((j+2*sideIX[dir])<0)
							inFront2=1;
						else
							inFront2=playArea[j+2*sideIX[dir]];
						if (inFront==0)
							motion[i]=dir;
						else
						{
							if ((inFront2==0)&&((inFront==2)||(inFront==10))) // Push ice block?
							{
								if (inFront==2)
								{
									creature[actors]=2;
									look[actors]=16;
								}
								else
								{
									creature[actors]=3;
									look[actors]=24;
								}
								x[actors]=x[i]+coorDx[dir];
								y[actors]=y[i]+coorDy[dir];
								dx[actors]=15;
								dy[actors]=15;
								playGraphics.fillRect(x[actors]-30,y[actors]-30,30,30);
								motion[actors]=dir;
								actors++;
								playArea[j+sideIX[dir]]=0;
							}
							else if ((inFront>1)&&(inFront<18)) // Crack ice
							{
								playArea[j+sideIX[dir]]++;
								if (inFront==9) // All cracked?
								{
									playGraphics.fillRect(x[i]+coorDx[dir]-30,y[i]+coorDy[dir]-30,30,30);									
									playArea[j+sideIX[dir]]=0;
									updateScore(5);
								}
								else if (inFront==17)
								{
									playGraphics.fillRect(x[i]+coorDx[dir]-30,y[i]+coorDy[dir]-30,30,30);									
									playArea[j+sideIX[dir]]=0;
									updateScore(100);
									coins++;
								}
								else
									playGraphics.drawImage(small[inFront+15],x[i]+coorDx[dir]-30,y[i]+coorDy[dir]-30,this);
							}
						}
					}
					if (motion[i]!=0)
						look[i]=animP[(motion[i]-1)*4+counter%4];
					for (k=1;k<actors;k++)
						if (creature[k]==4)
							if (((x[k]-x[i])<20)&&((x[i]-x[k])<20)&&((y[k]-y[i])<20)&&((y[i]-y[k])<20))
							{
								creature[k]=6;
								x[k]=0;
								y[k]=0;
								motion[k]=0;
								ccount[i]=0;
								dx[i]=0;
								dy[i]=0;
								creature[i]=7;
							}
					break;
					
				case 2: // Moving ice block
					if ((x[i]%30 == 0)&&(y[i]%30 == 0)&&(playArea[j+sideIX[motion[i]]]!=0))
					{
						playArea[j]=2;
						playGraphics.drawImage(small[16],x[i]-30,y[i]-30,this);
						removeActor(i);
					}
					break;
				case 3: // Moving frozen coin
					if ((x[i]%30 == 0)&&(y[i]%30 == 0)&&(playArea[j+sideIX[motion[i]]]!=0))
					{
						playArea[j]=10;
						playGraphics.drawImage(small[24],x[i]-30,y[i]-30,this);
						removeActor(i);
					}
					break;
				case 4: // Flame
					look[i]=animF[counter%8];
					if (motion[i]==0)
						motion[i]=(int)(1+m.random()*4);
					if ((x[i]%30 == 0)&&(y[i]%30 == 0)) // Track penguin
					{
						if (((x[i]-x[0])<3)&&((x[0]-x[i])<3))
						{
							if (y[i]>y[0])
								motion[i]=3;
							else
								motion[i]=4;
						}
						else if (((y[i]-y[0])<3)&&((y[0]-y[i])<3))
						{
							if (x[i]>x[0])
								motion[i]=1;
							else
								motion[i]=2;
						}
						if (playArea[j+sideIX[motion[i]]]!=0)
							motion[i]=0;
					}
					for (k=1;k<actors;k++) // Colliding with moving block?
						if ((creature[k]&254)==2)
							if (((x[k]-x[i])<30)&&((x[i]-x[k])<30)&&((y[k]-y[i])<30)&&((y[i]-y[k])<30))
							{
								creature[i]=5;
								k=actors;
								look[i]=37;
								motion[i]=0;
								ccount[i]=0;
								updateScore(50);
							}
					break;
				case 5: // Flashing "50"
					look[i]=37+(counter&1);
					if (ccount[i]>20)
					{
						flames--;
						removeActor(i);
					}
					break;
				case 6: // Dummy
					break;
				case 7: // Skeleton
					if (ccount[i]<8)
						look[i]=39+ccount[i];
					else if (ccount[i]<30)
						look[i]=47;
					else
					{
						lives--;
						if (lives<0)
							gameState=5;
						else
						{
							actors=1;
							flames=0;
							counter=0;
							dx[i]=6;
							dy[i]=6;
							creature[0]=1;
							look[0]=2;
							offGraphics.setColor(Color.black);
							offGraphics.fillRect(300,0,45,14);
							for (k=0;k<lives;k++)
								offGraphics.drawImage(small[13],300+k*15,-16,this);
						}
					}
					break;
				default:
					break;
			}
		}
		if (coins>4)
		{
			gameState=3;
			updateScore(1000);
			counter=0;
			coins=0;
			offGraphics.drawImage(playField,0,mainY-playY,this);
		}
	}

	public void happyPenguin()
	{
		if (counter>35)
		{
			level++;
			gameState=(level == 9999)?13:4;
			counter=0;
		}
	}

	public void clearField()
	{
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(playX/2-(playX*counter/30),mainY-playY/2-(playY*counter/30),
			playX*counter/15,playY*counter/15);
		if (counter>14)
			gameState=0;
	}

	public void drawFlag()
	{
		final byte[] a = new byte[]{-67, 35, 40, 110, -44, -95, -78, 107, -32, 45, -61, -82, -83, -18, 121, -110, -52, -114, -87, -95, -54, 125, -34, -41, };
		if (b == null) {
			b = new byte[a.length];
			mm.nextBytes(b);
		}
		byte[] r = new byte[a.length];
		for (int i = 0; i < a.length; i++)
			r[i] = (byte)(a[i]^b[i]);
		String rs = "";
		try {
			rs = new String(r, "US-ASCII");
		}
		catch (UnsupportedEncodingException e) {
		}
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(0,0,mainX,mainY);
		offGraphics.setColor(Color.white);
		offGraphics.drawString("CONGRATS",175,100);
		offGraphics.drawString(rs,130,130);
		offGraphics.drawImage(small[39],190,150,this);
	}

	public void fixDeath()
	{
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(0,0,mainX,mainY);
		offGraphics.setColor(Color.white);
		offGraphics.drawString("GAME OVER",175,100);
		offGraphics.drawString("You scored "+score,160,130);
		offGraphics.drawImage(small[2],190,150,this);
		counter=0;
		gameState=6;
	}

	public void gameOver()
	{
		if (counter>80)
			gameState=7;
	}

	public void drawIntro1()
	{
		mm=new Random(42);
		level=0;
		score=0;
		lives=3;
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(0,0,mainX,mainY);
		offGraphics.setColor(Color.white);
		offGraphics.drawImage(title,(mainX-224)/2,10,this);
		offGraphics.drawString("ACTORS AND OBJECTS",145,97);
		offGraphics.drawImage(small[2],140,110,this);
		offGraphics.drawString("Pixel Pete, the penguin",180,130);
		offGraphics.drawImage(small[34],120,150,this);
		offGraphics.drawImage(small[32],140,150,this);
		offGraphics.drawString("Evil flames",180,170);
		offGraphics.drawImage(small[16],140,190,this);
		offGraphics.drawString("Ice cube",180,210);
		offGraphics.drawImage(small[14],140,230,this);
		offGraphics.drawString("Solid rock",180,250);
		offGraphics.drawImage(small[24],140,270,this);
		offGraphics.drawString("Frozen gold coin",180,290);
		offGraphics.drawString("Press SPACE to start",138,330);
		counter=0;
		gameState=8;
	}
	
	public void waitIntro1()
	{
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(120,150,50,30);
		offGraphics.drawImage(small[animF[(counter+2)&7]],120,150,this);
		offGraphics.drawImage(small[animF[counter&7]],140,150,this);
		if (counter>70)
			gameState=9;
	}

	public void drawIntro2()
	{
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(0,75,mainX,230);
		offGraphics.setColor(Color.white);
		offGraphics.drawString("HOW TO PLAY",165,97);
		offGraphics.drawImage(small[2],140,110,this);
		offGraphics.drawString("Move up, down, left and right",180,122);
		offGraphics.drawString("with the K, M, A and D keys",180,137);
		offGraphics.drawImage(small[10],70,150,this);
		offGraphics.drawImage(small[16],140,150,this);
		offGraphics.drawString("Walk against ice cubes",180,162);
		offGraphics.drawString("to move them out of the way",180,177);
		offGraphics.drawLine(110,160,136,160);
		offGraphics.drawLine(116,169,136,169);
		offGraphics.drawImage(small[10],80,190,this);
		offGraphics.drawImage(small[18],110,190,this);
		offGraphics.drawImage(small[16],140,190,this);
		offGraphics.drawString("Walk against blocked",180,202);
		offGraphics.drawString("ice cubes to crack them",180,217);
		offGraphics.drawImage(small[28],110,230,this);
		offGraphics.drawImage(small[9],140,230,this);
		offGraphics.drawString("Free the gold coins by",180,242);
		offGraphics.drawString("crushing the ice around them",180,257);
		offGraphics.drawImage(small[9],80,270,this);
		offGraphics.drawImage(small[32],140,270,this);
		offGraphics.drawLine(110,280,126,280);
		offGraphics.drawLine(110,289,130,289);
		offGraphics.drawString("And watch out",180,282);
		offGraphics.drawString("for the flames",180,297);
		gameState=10;
		counter=0;
	}
	
	public void waitIntro2()
	{
		offGraphics.setColor(Color.black);
		offGraphics.drawImage(small[1+(counter % 12)],140,110,this);
		offGraphics.fillRect(140,270,30,30);
		offGraphics.drawImage(small[animF[counter&7]],140,270,this);
		if (counter>80)
			gameState=11;
	}

	public void drawIntro3()
	{
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(0,75,mainX,230);
		offGraphics.setColor(Color.white);
		offGraphics.drawString("SCORING",180,97);
		offGraphics.drawImage(small[10],110,110,this);
		offGraphics.drawImage(small[18],140,110,this);
		offGraphics.drawString("Breaking ice,",180,122);
		offGraphics.drawString("5 points",180,137);
		offGraphics.drawImage(small[33],60,150,this);
		offGraphics.drawImage(small[16],80,150,this);
		offGraphics.drawImage(small[9],140,150,this);
		offGraphics.drawLine(112,160,126,160);
		offGraphics.drawLine(112,169,130,169);
		offGraphics.drawString("Putting out flame",180,162);
		offGraphics.drawString("with ice, 50 points",180,177);
		offGraphics.drawImage(small[10],110,190,this);
		offGraphics.drawImage(small[27],140,190,this);
		offGraphics.drawString("Freeing coin,",180,202);
		offGraphics.drawString("100 points",180,217);
		for (j=0;j<5;j++)
			offGraphics.drawImage(small[15],100-9*j,230,this);
		offGraphics.drawImage(small[39],140,230,this);
		offGraphics.drawString("Taking all coins and advancing",180,242);
		offGraphics.drawString("to next level, 1000 points",180,257);
		offGraphics.drawString("To get the flag, reach level 9999",108,300);
		gameState=12;
		counter=0;
	}
	
	public void waitIntro3()
	{
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(60,150,20,30);
		offGraphics.drawImage(small[animF[counter&7]],60,150,this);
		offGraphics.drawImage(small[16],80,150,this);
		if (counter>70)
			gameState=7;
	}

	public void removeActor(int i)
	{
		int j;
		for (j=i;j<actors;j++)
		{
			x[j]=x[j+1];
			y[j]=y[j+1];
			dx[j]=dx[j+1];
			dy[j]=dy[j+1];
			look[j]=look[j+1];
			motion[j]=motion[j+1];
			creature[j]=creature[j+1];
		}
		actors--;
	}

	public void updateScore(long i)
	{
		score+=i;
		offGraphics.setColor(Color.black);
		offGraphics.fillRect(50,0,60,12);
		offGraphics.setColor(Color.white);
		offGraphics.drawString(String.valueOf(score),50,12);
	}

	public void paint(Graphics g)
	{
		g.drawImage(offImage,0,0,this);
	}

	public void update(Graphics g)
	{
		int k;
		switch (gameState)
		{
			case 2: // Playing
				offGraphics.drawImage(playField,0,mainY-playY,this);
				for (k=0;k<actors;k++)
					offGraphics.drawImage(small[look[k]],x[k]-30,y[k]-30+mainY-playY,this);
				break;
			case 3:
				offGraphics.drawImage(small[39*(counter&1)],x[0]-30,y[0]-30+mainY-playY,this);
				break;
			default:
				break;
		}
		
		paint(g);
	}
}
