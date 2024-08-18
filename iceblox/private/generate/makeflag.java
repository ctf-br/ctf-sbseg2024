import java.util.Random;

public class makeflag
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
	long snooze=100,score;
	Thread game;
	Math m;
	Random mm;

    public static void main(String[] args) throws Exception
    {
        new makeflag();
    }

    public makeflag() throws Exception
    {
        final byte[] flag = "CTF-BR{a3441pO8JtWTscjh}".getBytes();
        final int LEVELS = 9999;

        mm = new Random(42);
		playArea=new int[(blockX+2)*(blockY+3)];

        for (level = 0; level < LEVELS; level++) {
            if (level>effMax)
                effLevel=effMax;
            else
                effLevel=level;
            buildMap();
        }

        byte[] key = new byte[flag.length];
        mm.nextBytes(key);
        byte[] ciphertext = new byte[key.length];
        for (int i = 0; i < key.length; i++)
            ciphertext[i] = (byte)(key[i] ^ flag[i]);
        
        System.out.print("new byte[]{");
        for (int i = 0; i < key.length; i++)
            System.out.print(String.valueOf(ciphertext[i]) + ", ");
        System.out.println("}");
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
    }
}
