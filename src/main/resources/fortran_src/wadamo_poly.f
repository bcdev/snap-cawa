      subroutine polyexp(inn,par,pot,out,dinn,dpar)
CF2PY INTENT(IN) :: inn, par,pot
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: dinn,dpar
CF2PY DOUBLE :: inn(dinn)
CF2PY DOUBLE :: par(dpar)
CF2PY DOUBLE :: pot
CF2PY DOUBLE :: out(dinn)
      integer dinn,dpar,i,j
      double precision inn(dinn)
      double precision par(dpar)
      double precision out(dinn)
      double precision xx,xp,pot
      do i=1,dinn
        xx=(inn(i)**pot)
        xp=xx**(dpar-1)
        out(i)=0.d0
        do j=1,dpar
          out(i)=out(i)+par(j)*xp
          xp=xp/xx
        enddo
        out(i)=dexp(out(i))
      enddo
      end
      
      subroutine polyexp1(inn,par,pot,out,dpar)
CF2PY INTENT(IN) :: inn, par,pot
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: dpar
CF2PY DOUBLE :: inn
CF2PY DOUBLE :: par(dpar)
CF2PY DOUBLE :: pot
CF2PY DOUBLE :: out
      integer dpar,j
      double precision inn
      double precision par(dpar)
      double precision out
      double precision xx,xp,pot
        xx=(inn**pot)
        xp=xx**(dpar-1)
        out=0.d0
        do j=1,dpar
          out=out+par(j)*xp
          xp=xp/xx
        enddo
        out=dexp(out)
      end

      subroutine poly(inn,par,out,dinn,dpar)
CF2PY INTENT(IN) :: inn, par,pot
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: dinn,dpar
CF2PY DOUBLE :: inn(dinn)
CF2PY DOUBLE :: par(dpar)
CF2PY DOUBLE :: pot
CF2PY DOUBLE :: out(dinn)
      integer dinn,dpar,i,j
      double precision inn(dinn)
      double precision par(dpar)
      double precision out(dinn)
      double precision xx,xp
      do i=1,dinn
        xx=(inn(i))
        xp=xx**(dpar-1)
        out(i)=0.d0
        do j=1,dpar
          out(i)=out(i)+par(j)*xp
          xp=xp/xx
        enddo
        out(i)=out(i)
      enddo
      end

      subroutine explog(inn,par,out,dinn)
CF2PY INTENT(IN) :: inn, par
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: dinn
CF2PY DOUBLE :: inn(dinn)
CF2PY DOUBLE :: par(2)
CF2PY DOUBLE :: out(dinn)
      integer dinn,i
      double precision inn(dinn)
      double precision par(2)
      double precision out(dinn)
      do i=1,dinn
        out(i) = inn(i)
        if (out(i) .lt. 0) out(i)= 0.d0
        out(i) = dexp(par(1) + par(2) * dlog(out(i)))
        if (out(i) .lt. 0) out(i)= 0.d0
        if (out(i) .gt. 1) out(i)= 1.d0
      enddo
      end

      subroutine timestep(u,n,m,dx,dy,error)
      double precision u(n,m)
      double precision dx,dy,dx2,dy2,dnr_inv,tmp,diff
      integer n,m,i,j
cf2py intent(in) :: dx,dy
cf2py intent(in,out) :: u
cf2py intent(out) :: error
cf2py intent(hide) :: n,m
      dx2 = dx*dx
      dy2 = dy*dy
      dnr_inv = 0.5d0 / (dx2+dy2)
      error = 0d0
      do 200,j=2,m-1
         do 100,i=2,n-1
            tmp = u(i,j)
            u(i,j) = ((u(i-1,j) + u(i+1,j))*dy2+
     &           (u(i,j-1) + u(i,j+1))*dx2)*dnr_inv
            diff = u(i,j) - tmp
            error = error + diff*diff
100     continue
200   continue
      error = sqrt(error)
      end
      
      
      